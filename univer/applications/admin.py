from django.contrib import admin

# Register your models here.
from applications.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "FIO", "work_experience", "time_created")
    list_display_links = ("id", "FIO")
    list_filter = ("watched", "approved")
    ordering = ("work_experience", "time_created")
    search_fields = ["FIO"]

    fieldsets = [
        (
            "Просмотрена / Принята",
            {
                "fields": [
                    "watched",
                    "approved",
                ]
            },
        ),
        (
            "Личная информация",
            {"fields": ["FIO", "FIO_manager", "name_of_division", "current_post"]},
        ),
        (
            "Профессиональная деятельность",
            {
                "fields": [
                    "work_experience",
                    "personal_achievements",
                    "motivational_letter",
                ]
            },
        ),
        ("Доп. информация", {"fields": ["time_created"]}),
    ]
