from django.contrib import admin

from .models import Project, Membership, Box, Template

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'git_url')

class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

class MembershipInline(admin.TabularInline):
    model = Membership
    readonly_fields = ('public_key', 'private_key')
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', '_members', 'box', 'template')
    list_filter = ('box', 'template')
    search_fields = ('name',)
    inlines = (MembershipInline,)

    def _members(self, obj):
        return ", ".join([str(m) for m in obj.members.all()])
    _members.short_description = "Members"

admin.site.register(Template, TemplateAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Project, ProjectAdmin)
