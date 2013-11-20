import os
import sh
import shutil
import tempfile
import yaml

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.template import Template as Django_template, Context
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from utils.ip import interface_ip
from utils.zip import ZipCreator

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
    _metadata = {}

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.git_url)

    @property
    def git(self):
        if not self._git:
            self._git = sh.git.bake(_cwd=self.local_repository_dir, _env={
                'GIT_SSH': os.path.join(settings.PROJECT_ROOT, "projects/scripts/loose_ssh.sh")
            })
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

    def archive_repository(self, destination, *archive_args):
        try:
            (fd, tar_file) = tempfile.mkstemp()
            self.git.archive("remotes/origin/%s" % self.git_ref, *archive_args, _out=tar_file)
            sh.tar("xf", tar_file, _cwd=destination)
        finally:
            if tar_file:
                os.remove(tar_file)

    def get_metadata(self, project):
        if project.id in self._metadata:
            return self._metadata[project.id]

        temp_dir = tempfile.mkdtemp()
        self.archive_repository(temp_dir, "--", "stackstrap/meta.yml")

        meta_file = os.path.join(temp_dir, "stackstrap", "meta.yml")
        self.render_file(meta_file, {'project': project})

        # read the meta file as load it as yaml
        with open(meta_file) as f:
            metadata = yaml.load(f)

        # cleanup the temp directory
        shutil.rmtree(temp_dir)

        self._metadata[project.id] = metadata

        return metadata

    def update_state_file(self, project):
        temp_dir = tempfile.mkdtemp()
        self.archive_repository(temp_dir, "--", "stackstrap/state.sls")
        shutil.copy(os.path.join(temp_dir, "stackstrap", "state.sls"), "/home/stackstrap/project_states/project-%d.sls" % project.id)
        shutil.rmtree(temp_dir)

    def update_pillar_file(self, project):
        pillar_file = "/home/stackstrap/project_pillars/project-%d.sls" % project.id
        pillar_data = {
            'project': serialize("python", [project])[0]['fields']
        }

        temp_dir = tempfile.mkdtemp()
        self.archive_repository(temp_dir, "--", "stackstrap/pillar.sls")
        temp_pillar_file = os.path.join(temp_dir, "stackstrap", "pillar.sls")
        if os.path.isfile(temp_pillar_file):
            shutil.copy(temp_pillar_file, "/home/stackstrap/project_pillars/project-%d.sls" % project.id)
        else:
            open(pillar_file, "w")
        shutil.rmtree(temp_dir)

        with open(pillar_file, "a") as f:
            f.write(yaml.safe_dump(pillar_data))

    def render_file(self, filename, context, replace=True):
        """
        Renders the specified filename using the Django template engine

        filename is the full path of the file to render
        context is the context to use when rendering
        replace if True the file will be rewritten as the same name, otherwise
                it will return the data
        """
        with open(filename, 'r') as f:
            t = Django_template(f.read())
        file_contents = t.render(Context(context))

        if replace:
            with open(filename, 'w') as f:
                f.write(file_contents)
        else:
            return file_contents


@receiver(models.signals.post_save, sender=Template)
def template_populate_cache(sender, instance, created, *args, **kwargs):
    if not created:
        return

    instance.create_local_repository()

@receiver(models.signals.post_save, sender=Template)
def update_template_project_state_files(sender, instance, created, *args, **kwargs):
    if created:
        return

    for project in instance.projects.all():
        instance.update_state_file(project)
        instance.update_pillar_file(project)


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
            help_text=_("The name of the project")
            )

    short_name = models.CharField(
            max_length=64,
            help_text=_("A URL and file system safe versAion of the name [a-z0-9_]"),
            validators=[RegexValidator(r'[a-z0-9_\.]+')]
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
            related_name='projects',
            blank=True,
            null=True,
            help_text=_("The template this project should use"))

    members = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            through='Membership'
            )

    def __unicode__(self):
        return self.name

    def make_project_zip(self, membership):
        with ZipCreator() as z:
            if self.template:
                self.template.archive_repository(z.temp_dir)

            z.mkdir('salt')
            z.mkdir('salt', 'keys')

            # build our context
            context = {
                    'project': self,
                    'membership': membership,
                    'master': settings.MASTER_HOSTNAME,
                    'master_ip': interface_ip(settings.MASTER_INTERFACE)
                    }

            # render our project template files that exist within the project app
            with open(z.path.join('Vagrantfile'), 'w') as f:
                f.write(render_to_string('projects/Vagrantfile', context))

            with open(z.path.join('salt', 'minion'), 'w') as f:
                f.write(render_to_string('projects/salt.minion', context))

            # put a file in place so our keys dir will exist in the zip and will
            # explain what the dir is and where to get the keys
            with open(z.path.join('salt', 'keys', 'README'), 'w') as f:
                f.write("You need to place **your** specific salt keys in this directory\n")
                f.write("Keys can be obtained from: http://%s/\n" % settings.MASTER_HOSTNAME)
                f.write("The .zip file you download should be extracted in this directory.\n")
                f.write("When complete you should have a minion.pub & minion.pem file in this directory\n")

            # make sure the salt keys are ignored in git repositories
            # we use append mode here so that we don't clobber an existing
            # .gitignore file
            with open(z.path.join('.gitignore'), 'a') as f:
                f.write("# Ignore local salt keys\n")
                f.write("salt/keys/*.p[eu][mb]\n")

            # process the stackstrap meta data
            metadata = self.template.get_metadata(self)

            # iterate the files to parse with Django templates
            file_template_paths = metadata.get("file_templates", [])
            file_template_paths.append("stackstrap/meta.yml")
            for path in file_template_paths:
                self.template.render_file(z.path.join(path), context)

            # iterate the paths to update with custom names
            path_templates = metadata.get("path_templates", [])
            for path_template in path_templates:
                for orig_path in path_template:
                    os.rename(z.path.join(orig_path),
                              z.path.join(path_template[orig_path]))

            return z.mkzip()

    def make_keys_zip(self, membership):
        with ZipCreator() as z:
            with open(z.path.join('minion.pem'), 'w') as f:
                f.write(membership.private_key.read())

            with open(z.path.join('minion.pub'), 'w') as f:
                f.write(membership.public_key.read())

            return z.mkzip()

@receiver(models.signals.post_save, sender=Project)
def update_project_state_files(sender, instance, created, *args, **kwargs):
    instance.template.update_state_file(instance)
    instance.template.update_pillar_file(instance)

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

    @property
    def minion_id(self):
        return 'user-%d-project-%d' % (
                self.user.id,
                self.project.id
                )

    @property
    def installed_public_key_filename(self):
        return "/etc/salt/pki/master/minions/%s" % self.minion_id

    def install_public_key(self):
        shutil.copy(self.public_key.file.name, self.installed_public_key_filename)

    def remove_public_key(self):
        if os.path.exists(self.installed_public_key_filename):
            os.remove(self.installed_public_key_filename)

@receiver(pre_save, sender=Membership)
def generate_keys(sender, instance, raw, *args, **kwargs):
    """
    If our public or private key is not set then auto generate them
    """
    if not instance.private_key or not instance.public_key:
        private_file = public_file = None

        try:
            (fd, private_file) = tempfile.mkstemp()
            sh.openssl.genrsa("-out", private_file, "2048")

            with open(private_file, 'r') as f:
                instance.private_key.save(
                        key_name(instance, '', '.pem'),
                        ContentFile(f.read()),
                        save=False
                        )

            (fd, public_file) = tempfile.mkstemp()
            sh.openssl.rsa("-in", private_file, "-pubout", "-out", public_file)

            with open(public_file, 'r') as f:
                instance.public_key.save(
                        key_name(instance, '', '.pub'),
                        ContentFile(f.read()),
                        save=False
                        )
        finally:
            if private_file:
                os.remove(private_file)

            if public_file:
                os.remove(public_file)


@receiver(post_save, sender=Membership)
def install_public_key(sender, instance, created, raw, *args, **kwargs):
    instance.install_public_key()

@receiver(pre_delete, sender=Membership)
def remove_member_public_key(sender, instance, *args, **kwargs):
    instance.remove_public_key()
