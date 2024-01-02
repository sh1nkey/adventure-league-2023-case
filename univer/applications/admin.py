from django.contrib import admin

# Register your models here.
from django.core.mail import send_mail

from applications.models import Application
from univer.settings import EMAIL_HOST_USER


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
            {
                "fields": [
                    "FIO",
                    "FIO_manager",
                    "name_of_division",
                    "current_post",
                    "email",
                ]
            },
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

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Application.objects.get(pk=obj.pk)
            if old_obj.watched != obj.watched and obj.watched:
                send_mail(
                    "Уведомление о заявке в корпоративный университет",
                    f"""Здравствуйте, {obj.FIO}!  
                    Ваше заявление просмотрели! Ожидайте ответа в течение следующих двух недель""",
                    EMAIL_HOST_USER,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
            elif old_obj.approved != obj.approved and obj.approved:
                send_mail(
                    "Уведомление о заявке в корпоративный университет",
                    f"""Здравствуйте, {obj.FIO}! 
                    Если вы ведите это сообщение, то Вас приняли в корпоративный университет совкомбанка!
                    Сердечно поздравляем! Ожидайте последующих указаний в течение недели.""",
                    EMAIL_HOST_USER,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
        super().save_model(
            request, obj, form, change
        )  # Call the original save_model method
