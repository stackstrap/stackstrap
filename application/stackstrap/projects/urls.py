from django.conf.urls import patterns, include, url

urlpatterns = patterns(
        '',

        url(r'(?P<project_id>\d+)/zip', 'projects.views.zip')
        )
