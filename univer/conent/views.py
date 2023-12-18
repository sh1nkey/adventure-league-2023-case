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

    @extend_schema(summary='Задачи и уч. материалы у предмета')
    def get(self, request, *args, **kwargs):
        return sub_task_material_get(self.request.user, self.kwargs.get("subject_id"))


class GetSingleTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return get_single_task(self.kwargs.get("task_id"))


class SendAnswers(CreateAPIView):
    """
    Создает и отправляет ответы на задание.

    Параметры запроса:
    - `body`: Данные с ответами.

    - path: ID задания, содержащее вопросы (ответы отправлять в том порядке, в котором присылаются)

    Возвращает:
    - Статус операции.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        return send_answers(
            data=request.data,
            user=self.request.user,
            task_id=self.kwargs.get("task_id"),
        )


class GetSubjects(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Статистика об общем прогрессе в предметах')
    def get(self, request, *args, **kwargs):
        return get_subjects_progress(self.request.user)


class GetStudyMaterial(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Получение подробных данных об уч. материале')
    def get(self, request, *args, **kwargs):
        return watch_material(self.request.user, self.kwargs.get("material_id"))


class TasksGet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer

    @extend_schema(summary='Получение невыполненных заданий')
    def get(self, request, *args, **kwargs):
        return get_tasks(self.request.user)
