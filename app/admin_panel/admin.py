from django.contrib import admin

from app.models.models import Categories, Projects, Tasks, TasksAssociation, User


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category_number", "category_title", "category_description")
    search_fields = ("category_title",)
    ordering = ("category_number",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "name", "surname", "email")
    search_fields = ("username", "email", "name", "surname")
    ordering = ("username",)


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ("id", "project_title", "project_category")
    search_fields = ("project_title",)
    list_filter = ("project_category",)


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ("id", "task_title", "task_description")
    search_fields = ("task_title",)


@admin.register(TasksAssociation)
class TasksAssociationAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "project", "user", "is_done")
    list_filter = ("is_done", "user", "project")
    search_fields = (
        "task__task_title",
        "project__project_title",
        "user__username",
    )
