from django.urls import path

from .views import (
    SubjectTaskMaterialGet,
    GetSingleTask,
    SendAnswers,
    GetSubjects,
    GetStudyMaterial,
    TasksGet,
)

urlpatterns = [
    path(
        "tasks-and-materials/<int:subject_id>",
        SubjectTaskMaterialGet.as_view(),
        name="get-tasks-materials",
    ),
    path("task/<int:task_id>", GetSingleTask.as_view(), name="get-task"),
    path(
        "study-material/<int:material_id>",
        GetStudyMaterial.as_view(),
        name="get-study-material",
    ),
    path("send-answers/<int:task_id>", SendAnswers.as_view(), name="answers-post"),
    path("subjects", GetSubjects.as_view(), name="get-subject"),
    path("tasks", TasksGet.as_view(), name="get-tasks"),
]
