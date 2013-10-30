import os
import shutil
import StringIO
import tempfile
import zipfile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Project, Membership

class ProjectsView(ListView):
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        """
        Return only projects the current user is a member of
        """
        return Project.objects.filter(membership__user=self.request.user)

class ZipDownload(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ZipDownload, self).dispatch(*args, **kwargs)

    def get(self, request, project_id):
        # look up the project & membership
        project = get_object_or_404(Project, id=project_id)
        membership = get_object_or_404(Membership, project=project, user=request.user)

        # get our temp dir
        temp_dir = tempfile.mkdtemp()
        temp_dir_len = len(temp_dir) + 1

        def temp_file(*args):
            "closure to make generating temp file names easier"
            return os.path.join(temp_dir, *args)

        # make the rest of our dirs
        os.mkdir(temp_file('salt'))
        os.mkdir(temp_file('salt', 'keys'))

        # build our context
        context = {
                'user': request.user,
                'project': project,
                'membership': membership,
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

        # send our response
        resp = HttpResponse(zip_io.getvalue(), mimetype = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=StackStrap-Project-Template_%d-%s.zip' % (project.id, project.name)
        return resp
