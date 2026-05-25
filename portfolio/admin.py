from django.contrib import admin
from .models import (
    Certificate, Experience, Education,
    Skill, Project, Interest, SocialLink
)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display  = ('name', 'organization', 'date_issued')
    list_filter   = ('organization',)
    search_fields = ('name', 'organization')
    ordering      = ('-date_issued',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display  = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter   = ('is_current',)
    ordering      = ('-start_date',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display  = ('degree', 'institution', 'start_year', 'end_year', 'is_current')
    ordering      = ('-start_year',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'level', 'order')
    list_filter   = ('category',)
    ordering      = ('order', 'name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'date', 'featured')
    list_filter   = ('featured',)
    search_fields = ('title',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order')