from django.db.models import Subquery
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from conent.models import Tasks, TaskResult, StudyMaterials, Subjects
from conent.serializers import (
    TaskResultSerializer,
    AnswerSerializer,
    TasksSerializer,
)
from conent.utils import get_single_task, send_answers, get_subjects_progress, sub_task_material_get
from users.models import StudentProfile


class SubjectTaskMaterialGet(APIView):
    """Нужен для получения задач и учебных материалов по ID предмета"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "OK", 400: "Bad Request"},
        operation_description="""Request: None\n Auth: Mandatory
        Response:
    [
        {
        "subject" : "Матан",
        "name" : "Лекция 1"
        }
    ].
    """,
    )
    def get(self, request, *args, **kwargs):
        return sub_task_material_get(self.request.user, self.kwargs.get("subject_id"))


class GetSingleTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return get_single_task(self.kwargs.get("task_id"))


class SendAnswers(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer

    @swagger_auto_schema(
        request_body=AnswerSerializer(many=True),  # Сериализатор для запроса
        responses={
            200: openapi.Response("OK", TaskResultSerializer)
        },  # Сериализатор для ответа
        operation_description="Ответов много. Response - результат проверки",
    )
    def create(self, request, *args, **kwargs):
        return send_answers(
            data=request.data,
            user=self.request.user,
            task_id=self.kwargs.get("task_id")
        )


class GetSubjects(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "OK", 400: "Bad Request"},
        operation_description="""Request: None\n Auth: Mandatory
        Response:
   [
  "Изучение африки"
    ]
    """,
    )
    def get(self, request, *args, **kwargs):
        return get_subjects_progress(self.request.user)


class GetStudyMaterial(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            study_material = StudyMaterials.objects.select_related("subject").get(
                id=self.kwargs.get("material_id")
            )
            user = self.request.user

            if user not in study_material.who_watched.all():
                study_material.who_watched.add(user)
                study_material.save()

            send_data = {
                "name": study_material.name,
                "subject": study_material.subject.name,
                "text": study_material.text,
            }

            return JsonResponse(send_data, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class TasksGet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            user_profile = StudentProfile.objects.select_related("group").get(user=user)

            tasks_with_results = TaskResult.objects.values("task_id").distinct()
            queryset = list(
                Tasks.objects.filter(groups=user_profile.group)
                .select_related("subject__name")
                .exclude(id__in=Subquery(tasks_with_results))
                .values("id", "name", "subject__name")
            )

            return JsonResponse(queryset, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
