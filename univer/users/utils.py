from datetime import datetime

from django.http import JsonResponse
from django.db.models import Case, When, Value, BooleanField

from conent.models import Tasks, StudyMaterials
from timetable.models import Day
from users.models import StudentProfile


def profile_data(user):
    try:
        """Общая информация"""
        user_profile = StudentProfile.objects.select_related("group").get(user=user)
        group = user_profile.group

        sending_data = [
            {
                "FIO": f"{user.surname} {user.name} {user.patronymic}",
                "status": user.role,
                "id": user.id,
                "period": user_profile.study_period,
                "group": group.name,
                "specialization": user_profile.specialization.name,
            }
        ]

        """Количество посещений"""
        quantity_of_visits = user_profile.quantity_of_visiting
        subjs = (
            Day.objects.filter(week__group=group).prefetch_related("subjtime").count()
        )

        today = datetime.now()
        current_year = datetime.now().year
        date_first_september = datetime(current_year, 9, 1)
        minus = today - date_first_september
        minus = minus.days - ((minus.days // 7) * 2)
        subjs *= minus // 7

        visiting_percentage = str(round(quantity_of_visits / subjs, 2) * 100) + " %"
        sending_data.append({"visiting_percentage": visiting_percentage})

        """Статистика по задачам"""
        tasks = (
            Tasks.objects.prefetch_related("taskresult_set")
            .filter(groups=group)
            .annotate(
                done_or_not=Case(
                    When(taskresult__isnull=False, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .values("id", "done_or_not")
            .distinct()
        )

        tasks_all_count = len(tasks)
        task_done_count = sum(1 for i in tasks if i["done_or_not"])

        sending_data.append(
            {
                "task_all": tasks_all_count,
                "task_done": task_done_count,
                "task_not_done": tasks_all_count - task_done_count,
            }
        )
        """Статистика по учебным материалам"""
        materials_done = (
            StudyMaterials.objects.prefetch_related("who_watched")
            .filter(who_watched=user)
            .values_list("id", flat=True)
        )
        materials_done_count = materials_done.count()

        materials_not_done_count = (
            StudyMaterials.objects.filter(
                group=group,
            )
            .exclude(id__in=materials_done)
            .count()
        )

        sending_data.append(
            {
                "material_all": materials_not_done_count + materials_done_count,
                "material_done": materials_done_count,
                "material_not_done": materials_not_done_count,
            }
        )

        return JsonResponse(sending_data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
