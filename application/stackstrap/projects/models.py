import os
import tempfile
import sh
import shutil
import StringIO
import subprocess
import tempfile
import zipfile
import yaml

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.template import Template as DjangoTemplate, Context
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


def key_name(instance, filename, extension):
    """
    Callable for the upload_to parameter of our membership files
    """
    return os.path.join('public_keys',
                        'project-%d' % instance.project.id,
                        "%s%s" % (
                            instance.user.email,
                            extension)
                        )

class Template(models.Model):
    """
    A template to use when creating projects
    """
    name = models.CharField(
            max_length=128,
            help_text=_("The name of this template"))

    git_url = models.CharField(
            max_length=255,
            help_text=_("The URL of the git repository that contains this template"))

    git_ref = models.CharField(
            max_length=64,
            default="master",
            help_text=_("The REF to use when applying the template to a project (ie. Git Tag or Branch)"))

    last_cache_update = models.DateTimeField(
            blank=True,
            null=True,
            help_text=_("The last time the local cache of the repository was updated"))

    _git = None

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.git_url)

    @property
    def git(self):
        if not self._git:
            self._git = sh.git.bake(_cwd=self.local_repository_dir)
        return self._git

    @property
    def local_repository_dir(self):
        return os.path.join(settings.MEDIA_ROOT, "template_repository_cache", str(self.id))

    def create_local_repository(self):
        if os.path.exists(self.local_repository_dir):
            raise RuntimeError(
                "We were asked to create the local repository for %s "
                "from the url %s, but the local dir (%s) already exists!"
                "Cowardly refusing to continue..." % (
                    self.name,
                    self.git_url,
                    self.local_repository_dir))

        os.makedirs(self.local_repository_dir)

        self.git.init('--bare')
        self.git.remote('add', 'origin', self.git_url)

        self.update_local_repository()

    def update_local_repository(self):
        self.git.fetch('origin')
        self.last_cache_update = now()
        self.save()

    def archive_repository(self, destination):
        archive_io = StringIO.StringIO()

        self.git.archive("remotes/origin/%s" % self.git_ref, _out=archive_io)

        sh.tar("xf", "-", _cwd=destination, _in=archive_io.getvalue())

@receiver(models.signals.post_save, sender=Template)
def template_populate_cache(sender, instance, created, *args, **kwargs):
    if not created:
        return

    instance.create_local_repository()

class Box(models.Model):
    """
    Holds the definition of our boxes that are used by projects
    """
    name = models.CharField(
            max_length=128,
            help_text=_("The name of this box"))

    url = models.URLField(
            max_length=255,
            help_text=_("The URL to download this box, as used by Vagrant"))

    class Meta:
        verbose_name_plural = 'Boxes'

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.url)


class Project(models.Model):
    """
    The model that holds our Project data
    """
    name = models.CharField(
            max_length=128,
            help_text=_("The name of the project, which should be succinct.")
            )

    slug = models.SlugField(
            max_length=128,
            help_text=_("A URL and file system safe version of the name")
            )

    description = models.TextField(
            blank=True,
            null=True,
            help_text=_("A free form desription of the project for organizational purposes")
            )

    box = models.ForeignKey(
            Box,
            help_text=_("The box this project should use"))

    template = models.ForeignKey(
            Template,
            blank=True,
            null=True,
            help_text=_("The template this project should use"))

    members = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            through='Membership'
            )

    def __unicode__(self):
        return self.name

    def make_zip(self, membership):
        # get our temp dir
        temp_dir = tempfile.mkdtemp()
        temp_dir_len = len(temp_dir) + 1

        # copy our template into the temp directory, if needed
        if self.template:
            self.template.archive_repository(temp_dir)

        def temp_file(*args):
            "closure to make generating temp file names easier"
            return os.path.join(temp_dir, *args)

        # make the rest of our dirs
        os.mkdir(temp_file('salt'))
        os.mkdir(temp_file('salt', 'keys'))

        # build our context
        context = {
                'project': self,
                'membership': membership,
                'user': membership.user,
                }

        # render our files
        with open(temp_file('Vagrantfile'), 'w') as f:
            f.write(render_to_string('projects/Vagrantfile', context))

        with open(temp_file('salt', 'minion'), 'w') as f:
            f.write(render_to_string('projects/salt.minion', context))

        with open(temp_file('salt', 'keys', 'minion.pem'), 'w') as f:
            f.write(membership.private_key.read())

        with open(temp_file('salt', 'keys', 'minion.pub'), 'w') as f:
            f.write(membership.public_key.read())

        def render_template(source):
            if isinstance(source, basestring):
                template_data = source
            else:
                template_data = source.read()
            tmpl = DjangoTemplate(template_data)
            return tmpl.render(Context(context))

        # read the metadata
        # apply the file & path templates
        if os.path.exists(temp_file('stackstrap')):
            # get the stackstrap yaml from the template
            with open(temp_file('stackstrap'), 'r') as yaml_file:
                metadata = yaml.load(yaml_file).get("stackstrap", {})

            # iterate the files to parse with django templates
            file_template_paths = metadata.get("file_templates", [])
            for path in file_template_paths:
                template_data = render_template(open(temp_file(path), 'r'))
                with open(temp_file(path), 'w') as template_file:
                    template_file.write(template_data)

            # iterate the paths to update with custom names
            path_templates = metadata.get("path_templates", [])
            for orig_path in path_templates:
                new_path = render_template(path_templates[orig_path])
                os.rename(temp_file(orig_path),temp_file(new_path))

        # build our zip file to be returned to the user
        zip_io = StringIO.StringIO()
        zip_file = zipfile.ZipFile(zip_io, "w")

        # recursively add our files
        for base, dirs, files in os.walk(temp_dir):
            for f in files:
                # build the full name
                zip_name = os.path.join(base, f)

                # write the file relative to the top of the temp dir
                zip_file.write(zip_name, zip_name[temp_dir_len:])

        zip_file.close()

        # clean up our tempdir
        shutil.rmtree(temp_dir)

        return zip_io.getvalue()

class Membership(models.Model):
    """
    Our through model for relating users and projects.

    It's primary purpose is to associate keys with the user + project combo
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project)

    public_key = models.FileField(
            upload_to=lambda i, f: key_name(i, f, '.pub')
            )
    private_key = models.FileField(
            upload_to=lambda i, f: key_name(i, f, '.pem')
            )

    def save(self, *args, **kwargs):
        """
        If our public or private key is not set then auto generate them
        """
        if not self.private_key or not self.public_key:
            private_file = public_file = None

            try:
                (fd, private_file) = tempfile.mkstemp()
                ret = subprocess.Popen([
                        "openssl", "genrsa",
                        "-out", private_file,
                        "2048"]
                        ).wait()

                with open(private_file, 'r') as f:
                    self.private_key.save(
                            key_name(self, '', '.pem'),
                            ContentFile(f.read()),
                            save=False
                            )

                (fd, public_file) = tempfile.mkstemp()
                ret = subprocess.Popen([
                        "openssl", "rsa",
                        "-in", private_file,
                        "-pubout",
                        "-out", public_file]
                        ).wait()

                with open(public_file, 'r') as f:
                    self.public_key.save(
                            key_name(self, '', '.pub'),
                            ContentFile(f.read()),
                            save=False
                            )

                # TODO: install the public_key in the master

            finally:
                if private_file:
                    os.remove(private_file)

                if public_file:
                    os.remove(public_file)

        super(Membership, self).save(*args, **kwargs)

    @property
    def minion_id(self):
        return 'user-%d-project-%d' % (
                self.user.id,
                self.project.id
                )
