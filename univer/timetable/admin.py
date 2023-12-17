from django.contrib import admin

# Register your models here.
from timetable.models import Day, Week, SubjTime



@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("id", "day_of_the_week")
    list_display_links = ("id", "day_of_the_week")


@admin.register(SubjTime)
class DayAdmin(admin.ModelAdmin):
    pass


class SubjPartInline(
    admin.TabularInline
):  # Используем TabularInline или StackedInline в зависимости от предпочтений отображения
    model = SubjTime
    extra = 1


class DaysInline(
    admin.TabularInline
):  # Используем TabularInline или StackedInline в зависимости от предпочтений отображения
    model = Day
    extra = 1
    inline = [SubjPartInline]


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "even_or_uneven")
    list_display_links = ("id", "group")
    inlines = [DaysInline]
    search_fields = ["group__name"]
