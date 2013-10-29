import os
import tempfile
import subprocess

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
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

class Project(models.Model):
    """
    The model that holds our Project data
    """
    name = models.CharField(
            max_length=128,
            help_text=_("The name of the project")
            )

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
