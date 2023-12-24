import datetime

from django.db import models

# Create your models here.


class Application(models.Model):
    FIO = models.CharField(max_length=60, verbose_name="ФИО инициатора")
    FIO_manager = models.CharField(max_length=60, verbose_name="ФИО руководителя")
    name_of_division = models.CharField(
        max_length=60, verbose_name="Наименование подразделения"
    )
    current_post = models.CharField(max_length=60, verbose_name="Текущая должность")
    personal_achievements = models.CharField(
        max_length=600,
        verbose_name="Личные достижения в компании за последние 12 месяцев",
    )
    motivational_letter = models.TextField(
        max_length=1000, verbose_name="Мотивационное письмо"
    )

    work_experience = models.IntegerField(verbose_name="Стаж работы в месяцах")
    time_created = models.DateTimeField(
        default=datetime.datetime.now(), verbose_name="Время подачи заявки"
    )

    approved = models.BooleanField(default=0, verbose_name="Принят ли в университет")
    watched = models.BooleanField(default=0, verbose_name="Просмотрена ли анкета")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
