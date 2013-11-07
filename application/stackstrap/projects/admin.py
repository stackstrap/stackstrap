from django.conf.urls.defaults import patterns
from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from .models import Project, Membership, Box, Template

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'git_url')

    def get_urls(self):
        urls = super(TemplateAdmin, self).get_urls()
        return patterns('',
            (r'(?P<template_id>\d+)/update_repository/$', self.admin_site.admin_view(self.update_repository)),
        ) + urls

    def update_repository(self, request, template_id):
        template = Template.objects.get(id=template_id)
        template.update_local_repository()
        messages.success(request, "Successfully updated local repository cache")
        return HttpResponseRedirect('..')


class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

class MembershipInline(admin.TabularInline):
    model = Membership
    readonly_fields = ('public_key', 'private_key')
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', '_members', 'box', 'template')
    list_filter = ('box', 'template')
    search_fields = ('name',)
    inlines = (MembershipInline,)

    def _members(self, obj):
        return ", ".join([str(m) for m in obj.members.all()])
    _members.short_description = "Members"

admin.site.register(Template, TemplateAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Project, ProjectAdmin)
