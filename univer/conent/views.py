from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from conent.serializers import (
    AnswerSerializer,
    TasksSerializer,
)
from conent.utils import (
    get_single_task,
    send_answers,
    get_subjects_progress,
    sub_task_material_get,
    watch_material,
    get_tasks,
)


class SubjectTaskMaterialGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return sub_task_material_get(self.request.user, self.kwargs.get("subject_id"))


class GetSingleTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return get_single_task(self.kwargs.get("task_id"))


class SendAnswers(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer

    # @extend_schema_view(summary="Нужен для получения задач и учебных материалов по ID предмета")
    def create(self, request, *args, **kwargs):
        return send_answers(
            data=request.data,
            user=self.request.user,
            task_id=self.kwargs.get("task_id"),
        )


class GetSubjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return get_subjects_progress(self.request.user)


class GetStudyMaterial(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return watch_material(self.request.user, self.kwargs.get("material_id"))


class TasksGet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer

    def list(self, request, *args, **kwargs):
        return get_tasks(self.request.user)
