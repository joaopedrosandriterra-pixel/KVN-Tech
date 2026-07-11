from django.contrib import admin

from .models import CaseStudy, Contact, Project, ProjectImage, ProjectUpdate, RoadmapItem, Technology


class RoadmapItemInline(admin.TabularInline):
    model = RoadmapItem
    extra = 1


class ProjectUpdateInline(admin.StackedInline):
    model = ProjectUpdate
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'visible', 'featured', 'updated_at')
    list_filter = ('visible', 'featured')
    search_fields = ('title', 'client_name', 'segment', 'challenge', 'solution')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'progress', 'visible', 'featured', 'updated_at')
    list_filter = ('status', 'visible', 'featured', 'technologies')
    search_fields = ('title', 'short_description', 'full_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)
    inlines = [RoadmapItemInline, ProjectUpdateInline, ProjectImageInline]


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'email', 'phone', 'budget', 'deadline', 'created_at')
    list_filter = ('service', 'budget', 'deadline', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone', 'message', 'dynamic_data')

