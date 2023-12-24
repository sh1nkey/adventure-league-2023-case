import datetime

from django.db import models

# Create your models here.
from users.models import Group, User


class Subjects(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название предмета")
    groups = models.ManyToManyField(
        Group, blank=True, verbose_name="Группы, у которых есть этот предмет"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Tasks(models.Model):
    name = models.CharField(max_length=50, null=True, verbose_name="Задача для решения")
    groups = models.ManyToManyField(Group, verbose_name="Каким группам её выдать")
    subject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, verbose_name="Предмет", null=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Задание для студентов"
        verbose_name_plural = "Задания для студентов"


class Questions(models.Model):
    text = models.CharField(max_length=300, verbose_name="Текст вопроса")
    right_answer = models.CharField(
        max_length=10, verbose_name="Правильный ответ на вопрос"
    )
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    answer = models.CharField(max_length=10, verbose_name="Ответ студента")
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Чей ответ"
    )
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, verbose_name="На какой вопрос"
    )

    def __str__(self):
        return f"{self.answer}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class TaskResult(models.Model):
    task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, verbose_name="Какое задание"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Кто прошел"
    )
    correct_percentage = models.FloatField(
        max_length=3, verbose_name="Процент правильности заданий"
    )
    time_created = models.DateTimeField(
        default=datetime.datetime.now(), verbose_name="Дата и время прохождения"
    )

    def __str__(self):
        return f"{self.task.name} {self.student.surname}"

    class Meta:
        verbose_name = "Результат прохождения задания"
        verbose_name_plural = "Результаты прохождений заданий"


class StudyMaterials(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название учебного материала")
    text = models.CharField(
        max_length=600, null=True, blank=True, verbose_name="Текст учебного материала"
    )
    subject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, verbose_name="Предмет"
    )
    # сделать поле с файлом
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Для какой группы учебный материал",
    )
    who_watched = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"


# реализовать расписание
