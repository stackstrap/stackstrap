from django.contrib import admin

from .models import Project, Membership

class MembershipInline(admin.TabularInline):
    model = Membership
    readonly_fields = ('public_key', 'private_key')
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (MembershipInline,)

admin.site.register(Project, ProjectAdmin)
