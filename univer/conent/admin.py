from django.contrib import admin

# Register your models here.
from conent.models import Subjects, Questions, Tasks, Answer, TaskResult, StudyMaterials


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    list_display_links = ("id", "text")
    list_filter = ["task"]


class QuestionsInline(
    admin.TabularInline
):  # Используем TabularInline или StackedInline в зависимости от предпочтений отображения
    model = Questions
    extra = 1  # Количество дополнительных пустых форм


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "answer", "student")
    list_display_links = ("id", "answer")
    search_fields = ["student__surname", "student__name"]


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    list_filter = ("groups",)
    inlines = [QuestionsInline]


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "student", "correct_percentage", "time_created")
    list_display_links = ("id",)
    list_filter = ["student__group"]


@admin.register(StudyMaterials)
class StudyMaterialsAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "name")
    list_display_links = ("id", "group")
    search_fields = ["name"]
    list_filter = ["subject__name", "group__name"]
