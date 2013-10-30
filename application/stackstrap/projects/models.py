import os
import tempfile
import subprocess

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from git import Repo

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
            help_text=_("The URL of the git repository that contains this template (master branch)"))

    last_cache_update = models.DateTimeField(
            blank=True,
            null=True,
            help_text=_("The last time the local cache of the repository was updated"))

    _repo = None

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.git_url)

    @property
    def local_repository_dir(self):
        return os.path.join(settings.MEDIA_ROOT, "template_repository_cache", str(self.id))

    @property
    def repo(self):
        if not self._repo:
            self._repo = Repo(self.local_repository_dir)
        return self._repo

    def create_local_repository(self):
        if os.path.exists(self.local_repository_dir):
            raise RuntimeError(
                "We were asked to create the local repository for %s "
                "from the url %s, but the local dir (%s) already exists!"
                "Cowardly refusing to continue..." % (
                    self.name,
                    self.git_url,
                    self.local_repository_dir))

        #Repo.init(self.local_repository_dir, bare=True)
        Repo.init(self.local_repository_dir)

        self.repo.create_remote('origin', self.git_url)
        self.update_local_repository()

    def update_local_repository(self):
        self.repo.remotes.origin.fetch()
        self.last_cache_update = now()
        self.save()

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
            help_text=_("The name of the project")
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
