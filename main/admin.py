from django.contrib import admin

from .models import Project, ProjectImage, ProjectUpdate, RoadmapItem, Technology


class RoadmapItemInline(admin.TabularInline):
    model = RoadmapItem
    extra = 1


class ProjectUpdateInline(admin.StackedInline):
    model = ProjectUpdate
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


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
