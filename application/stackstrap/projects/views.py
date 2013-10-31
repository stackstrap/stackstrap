from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Project, Membership

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ProjectsView(LoginRequiredMixin, ListView):
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        """
        Return only projects the current user is a member of
        """
        return Project.objects.filter(membership__user=self.request.user)

class ProjectDownloadView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        # look up the project & membership
        self.project = get_object_or_404(Project, id=project_id)
        self.membership = get_object_or_404(Membership, project=self.project, user=request.user)

        # return our response
        return self.get_response()

    def get_response(self):
        raise NotImplemented("You need to implement this in your subclass")

class ZipDownload(ProjectDownloadView):
    def get_response(self):
        resp = HttpResponse(self.project.make_project_zip(self.membership), mimetype = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=StackStrap_%d-%s.zip' % (self.project.id, self.project.name)
        return resp

class KeyDownload(ProjectDownloadView):
    def get_response(self):
        resp = HttpResponse(self.project.make_keys_zip(self.membership), mimetype = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=StackStrap-Keys_%s-%d-%s.zip' % (
                self.membership.user.email,
                self.project.id,
                self.project.name)
        return resp
