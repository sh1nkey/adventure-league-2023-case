from django.db.models import F
from django.http import JsonResponse


# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from conent.models import Subjects
from timetable.models import Week
from timetable.serializer import SubjNameSerializer, StudentSurnameSerializer
from users.models import StudentProfile


class ShowTimetable(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "if_even", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            user_profile = StudentProfile.objects.get(user=user)
            if_even = True if self.request.query_params.get("if_even") == 'true' else False

            week_with_days = Week.objects.prefetch_related(
                "day_set", "day_set__part_of_timetable"
            ).get(group=user_profile.group, even_or_uneven=if_even)

            sending_data = []
            days_of_the_week = (
                "Понедельник",
                "Вторник",
                "Среда",
                "Четверг",
                "Пятница",
                "Суббота",
            )

            times = (
                "8.30 - 10.10",
                "10.20 - 12.00",
                "12.20 - 14.00",
                "14.10 - 15.50",
                "16.00 - 17.40",
                "18.00 - 19.30",
                "19.40 - 21.10",
                "21.20 - 22.50",
            )

            for i in range(1, 7):
                day = (
                    week_with_days.day_set.filter(day_of_the_week=i)
                    .order_by("day_of_the_week")
                    .first()
                )
                if day is None:
                    sending_data.append(
                        {"day_of_the_week": days_of_the_week[i - 1], "subjects": None}
                    )
                    continue
                sending_data.append(
                    {"day_of_the_week": days_of_the_week[i - 1], "subjects": []}
                )
                for j in day.part_of_timetable.all().order_by("pair_number"):
                    sending_data[i - 1]["subjects"].append(
                        {"subject": j.subject.name, "time": times[j.pair_number]}
                    )
            return JsonResponse(sending_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class SubjectsGet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjNameSerializer
    queryset = Subjects.objects.all().values("name").order_by("name")


class GroupGet(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "subj_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        subj_name = self.request.query_params.get("subj_name")

        sending_data = list(
            Subjects.objects.filter(name=subj_name).values("groups__name")
        )

        return JsonResponse(sending_data, safe=False, status=200)


class StudGet(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "group_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        group_name = self.request.query_params.get("group_name")

        users_profile = list(
            StudentProfile.objects.filter(group__name=group_name)
            .values("user__surname", "user__name", "user__patronymic")
            .order_by("user__surname")
        )

        return JsonResponse(users_profile, safe=False, status=200)


class MarkVisitors(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjNameSerializer(many=True)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"student__surname": openapi.Schema(type=openapi.TYPE_STRING)},
        )
    )
    def post(self, request, *args, **kwargs):
        serializer = StudentSurnameSerializer(data=request.data, many=True)
        if serializer.is_valid():
            data = request.data

            students = StudentProfile.objects.filter(
                user__surname__in=[student["student__surname"] for student in data]
            )

            students.update(quantity_of_visiting=F("quantity_of_visiting") + 1)

        return JsonResponse(
            {"result": f"Отмечено {students.count()} человек"}, status=200
        )
