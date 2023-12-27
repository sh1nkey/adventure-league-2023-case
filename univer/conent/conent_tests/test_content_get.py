import json

import pytest

from django.urls import reverse

from users.models import User
from ..models import Subjects
from .fixtures import (
    create_task_record,
    log_in_user,
    create_many_task_records,
    group_create,
    subject_create,
    create_study_material,
    create_task_and_study_material
)

# ---------- Test Task  ----------


@pytest.mark.django_db
def test_get_single_task_should_return_single_record(
        client, create_task_record, log_in_user
) -> None:
    response = client.get(
        reverse("get-task", kwargs={"task_id": 1}),
        headers={"Authorization": f"Bearer {log_in_user['token']}"},
    )

    assert response.status_code == 200
    assert json.loads(response.content)["name"] == "Example Task"


@pytest.mark.django_db
def test_tasks_should_return_many_records(
        client, create_many_task_records, log_in_user
) -> None:
    response = client.get(
        reverse("get-tasks"),
        headers={"Authorization": f"Bearer {log_in_user['token']}"},
    )

    result = json.loads(response.content)
    assert response.status_code == 200
    assert result[0]["name"] == "Example Task 1"
    assert result[1]["name"] == "Example Task 2"
    assert len(result) == 2


# ---------- Test Subjects  ----------


@pytest.mark.django_db
def test_subjects_should_return_one(
        client, log_in_user, create_task_record, group_create
) -> None:
    group = group_create
    group.students.add(User.objects.get(id=1))
    subj = Subjects.objects.get(id=1)
    subj.groups.add(group)

    response = client.get(
        reverse("get-subject"),
        headers={"Authorization": f"Bearer {log_in_user['token']}"},
    )

    result = json.loads(response.content)

    assert response.status_code == 200
    assert len(result) == 1
    assert result[0]["subject"] == "Тестовый предмет"


# ---------- Test StudyMaterial ----------
@pytest.mark.django_db
def test_get_single_study_material_should_succeed(
        client, log_in_user, create_study_material
) -> None:
    response = client.get(
        reverse("get-study-material", kwargs={"material_id": 1}),
        headers={"Authorization": f"Bearer {log_in_user['token']}"},
    )
    result = json.loads(response.content)

    assert response.status_code == 200
    assert result["name"] == "Тестовая статья"


# ---------- Test mixed endpoints ----------

@pytest.mark.django_db
def test_subject_task_material_get(
        client, create_task_and_study_material
) -> None:
    response = client.get(
        reverse("get-tasks-materials",
                kwargs={"subject_id": create_task_and_study_material['subject'].id}),
        headers={"Authorization": f"Bearer {create_task_and_study_material['user']}"},
    )
    result = json.loads(response.content)

    assert response.status_code == 200
    assert len(result) == 2
    assert result[0]['name'] == 'Example Task'
    assert result[1]['name'] == 'Тестовая статья'
