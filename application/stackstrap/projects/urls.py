from django.conf.urls import patterns, include, url

from .views import ProjectsView, ZipDownload

urlpatterns = patterns(
        '',

        url(r'(?P<project_id>\d+)/zip', ZipDownload.as_view(), name='project_zip'),
        url(r'', ProjectsView.as_view(), name='projects')
        )
