from datetime import datetime

from django.http import JsonResponse

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from conent.models import Tasks, StudyMaterials
from timetable.models import Week, SubjTime, Day
from users.models import User, StudentProfile
from users.serializers import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterUser(CreateAPIView):
    """
    Касаемо ролей, там будет выбор между четырьмя:
    1 - абитуриент
    2 - студент
    3 - куратор
    4 - преподаватель
    5 - приёмная комиссия
    """

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.create(**self.request.data)
            user.set_password(self.request.data.get("password"))
            user.save()

            from rest_framework_simplejwt.tokens import RefreshToken

            return JsonResponse(get_tokens_for_user(user), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)


class LogoutUser(APIView):
    """
    Возвращает {}
    """

    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return JsonResponse({}, status=200)


class ProfileGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            user_profile = StudentProfile.objects.get(user=user)
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

            quantity_of_visits = user_profile.quantity_of_visiting

            weeks = Week.objects.filter(group=group)
            days = Day.objects.filter(week__in=weeks)
            quantity_of_subjects = SubjTime.objects.filter(day__in=days).count()

            today = datetime.now()
            current_year = datetime.now().year
            date_first_september = datetime(current_year, 9, 1)
            minus = today - date_first_september

            minus = minus.days - ((minus.days // 7) * 2)
            quantity_of_subjects *= minus // 7

            visiting_percentage = (
                str(round(quantity_of_visits / quantity_of_subjects, 2) * 100) + " %"
            )

            sending_data.append({"visiting_percentage": visiting_percentage})

            tasks_with_results = Tasks.objects.filter(groups=group).prefetch_related(
                "taskresult_set"
            )
            study_materials = StudyMaterials.objects.filter(
                group=group
            ).prefetch_related("who_watched")

            done_task_ids = []
            for task in tasks_with_results:
                if task.taskresult_set.filter(student=user).exists():
                    done_task_ids.append(task.id)
            done_task = tasks_with_results.filter(id__in=done_task_ids)
            not_done_task = tasks_with_results.exclude(id__in=done_task_ids)

            done_study_materials = study_materials.filter(who_watched=user)
            done_sm_ids = done_study_materials.values_list("id", flat=True)
            not_done_sm = study_materials.exclude(id__in=done_sm_ids)

            sending_data.append(
                {
                    "material_all": len(study_materials),
                    "material_done": len(done_study_materials),
                    "material_not_done": len(not_done_sm),
                }
            )

            sending_data.append(
                {
                    "task_all": Tasks.objects.filter(groups=group).count(),
                    "task_done": len(done_task),
                    "task_not_done": len(not_done_task),
                }
            )

            return JsonResponse(sending_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
