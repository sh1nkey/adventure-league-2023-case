import json

import pytest

from django.urls import reverse

from users.models import Group, User
from .fixtures import create_task_record, log_in_user_token, create_many_task_records

# ---------- Test Task  ----------
from ..models import Subjects


@pytest.mark.django_db
def test_get_single_task_should_return_single_record(
    client, create_task_record, log_in_user_token
) -> None:
    response = client.get(
        reverse("get-task", kwargs={"task_id": 1}),
        headers={"Authorization": f"Bearer {log_in_user_token}"},
    )

    assert response.status_code == 200
    assert json.loads(response.content)["name"] == "Example Task"


@pytest.mark.django_db
def test_tasks_should_return_many_records(
    client, create_many_task_records, log_in_user_token
):
    response = client.get(
        reverse("get-tasks"),
        headers={"Authorization": f"Bearer {log_in_user_token}"},
    )

    result = json.loads(response.content)
    assert response.status_code == 200
    assert result[0]["name"] == "Example Task 1"
    assert result[1]["name"] == "Example Task 2"
    assert len(result) == 2


# ---------- Test Subjects  ----------

@pytest.mark.django_db
def test_subjects_should_return_one(client, log_in_user_token, create_task_record):
    group = Group.objects.create(name='ПИН-23-2')
    group.students.add(User.objects.get(id=1))
    subj = Subjects.objects.get(id=1)
    subj.groups.add(group)

    response = client.get(
        reverse("get-subject"),
        headers={"Authorization": f"Bearer {log_in_user_token}"},
    )

    result = json.loads(response.content)
    print('lmao', result)

    assert response.status_code == 200
    assert len(result) == 1
    assert result[0]["subject"] == "Тестовый предмет"
