from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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

        # send our response
        resp = HttpResponse(project.make_zip(membership), mimetype = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=StackStrap_%d-%s.zip' % (project.id, project.name)
        return resp
