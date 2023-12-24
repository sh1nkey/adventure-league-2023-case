from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(
        max_length=30, null=False, verbose_name="Имя", default="Ноунейм"
    )
    surname = models.CharField(
        max_length=30, null=False, verbose_name="Фамилия", default="Ноунеймов"
    )
    patronymic = models.CharField(
        max_length=30, null=False, verbose_name="Отчество", default="Ноунеймович"
    )

    ROLE_GROUP_CHOICES = (
        (1, "Абитуриент"),
        (2, "Студент"),
        (3, "Куратор"),
        (4, "Преподаватель"),
        (5, "Приёмная комиссия"),
    )
    role = models.IntegerField(null=False, default=1, choices=ROLE_GROUP_CHOICES)

    def __str__(self):
        return f"{self.surname} {self.name}"


class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexes_choice = ((0, "Женский"), (1, "Мужской"))
    sex = models.BooleanField(verbose_name="Пол", choices=sexes_choice, null=True)


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название группы")
    students = models.ManyToManyField(User, blank=True, verbose_name="Студенты группы")

    def __str__(self):
        return f"Группа {self.name}"

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Specialization(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название направления")
    groups = models.ManyToManyField(Group, verbose_name="Группы направления")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"


class StudentProfile(BaseProfile):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Группа",
        help_text="К какой группе принадлежит",
        null=True,
    )
    study_period = models.CharField(
        max_length=10, null=True, verbose_name="Срок обучения"
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name="Направление",
    )
    quantity_of_visiting = models.IntegerField(
        default=0, verbose_name="Количество посещений"
    )

    def __str__(self):
        return f"{self.id}   {self.user.surname} {self.user.name[0]}. {self.user.patronymic[0]}."

    class Meta:
        verbose_name = "Профиль студента"
        verbose_name_plural = "Профили студентов"


class TeacherProfile(BaseProfile):
    groups = models.ManyToManyField(
        Group, verbose_name="Группы", help_text="У каких групп ведёт"
    )

    class Meta:
        verbose_name = "Профиль преподавателя"
        verbose_name_plural = "Профили преподавателей"


#
