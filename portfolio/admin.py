from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Resume
from .models import (
    Certificate, Experience, Education,
    Skill, Project, Interest, SocialLink
)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    
@admin.register(Certificate)
class CertificateAdmin(ImportExportModelAdmin):
    list_display = ('name', 'organization', 'date_issued')
    list_filter = ('organization',)
    search_fields = ('name', 'organization')
    ordering = ('-date_issued',)


@admin.register(Experience)
class ExperienceAdmin(ImportExportModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    ordering = ('-start_date',)


@admin.register(Education)
class EducationAdmin(ImportExportModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year', 'is_current')
    ordering = ('-start_year',)


@admin.register(Skill)
class SkillAdmin(ImportExportModelAdmin):
    list_display = ('name', 'category', 'level', 'order')
    list_filter = ('category',)
    ordering = ('order', 'name')


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('title', 'date', 'featured')
    list_filter = ('featured',)
    search_fields = ('title',)


@admin.register(Interest)
class InterestAdmin(ImportExportModelAdmin):
    list_display = ('name', 'icon', 'order')


@admin.register(SocialLink)
class SocialLinkAdmin(ImportExportModelAdmin):
    list_display = ('platform', 'url', 'order')