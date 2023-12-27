import json

import pytest

from django.urls import reverse

from .fixtures import (
    create_task_record,
    log_in_user,
    create_many_task_records,
    group_create,
    subject_create,
    create_study_material,
    create_task_and_study_material,
    create_questions_for_task,
)
from ..models import Questions


@pytest.mark.django_db
def test_send_answers_should_succeed(
        client, log_in_user, create_questions_for_task
):
    task = create_questions_for_task
    data = [
        {
            'answer_data': 'Да.'
        },
        {
            'answer_data': 'Тоже да..',
        }
    ]
    response = client.post(
        reverse("answers-post", kwargs={"task_id": task.id}),
        data=json.dumps(data),
        content_type="application/json",
        headers={"Authorization": f"Bearer {log_in_user['token']}"},
    )
    result = json.loads(response.content)

    assert response.status_code == 201
    assert result['correct_percentage'] == 0.5
    