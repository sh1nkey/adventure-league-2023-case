from django.db import models

# Create your models here.
from conent.models import Subjects
from users.models import Group


class Week(models.Model):
    even_or_uneven = models.BooleanField(verbose_name="Чётная?", default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group.name} {"чётная" if self.even_or_uneven else "нечётная"}'

    class Meta:
        verbose_name = "Расписание по неделям"
        verbose_name_plural = "Расписания по неделям"


PAIR_NUMBER_CHOICE = (
    (1, "8.30 - 10.10"),
    (2, "10.20 - 12.00"),
    (3, "12.20 - 14.00"),
    (4, "14.10 - 15.50"),
    (5, "16.00 - 17.40"),
    (6, "18.00 - 19.30"),
    (7, "19.40 - 21.10"),
    (8, "21.20 - 22.50"),
)


class SubjTime(models.Model):
    pair_number = models.IntegerField(
        choices=PAIR_NUMBER_CHOICE, null=True, verbose_name="Номер пары (порядковый)"
    )
    subject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, null=True, verbose_name="Предмет"
    )

    def __str__(self):
        return f"{self.subject}  {self.pair_number}"

    class Meta:
        verbose_name = "Ячейка расписания"
        verbose_name_plural = "Ячейки расписания"


DAYS_OF_THE_WEEK_CHOICE = (
    (1, "Понедельник"),
    (2, "Вторник"),
    (3, "Среда"),
    (4, "Четверг"),
    (5, "Пятница"),
    (6, "Суббота"),
)


class Day(models.Model):
    day_of_the_week = models.IntegerField(
        verbose_name="День недели",
        choices=DAYS_OF_THE_WEEK_CHOICE,
        null=True,
        blank=True,
    )
    part_of_timetable = models.ManyToManyField(
        SubjTime, verbose_name="Предметы и их время"
    )
    week = models.ForeignKey(
        Week, on_delete=models.CASCADE, null=True, verbose_name="Неделя"
    )

    class Meta:
        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"
