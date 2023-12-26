import json
from datetime import datetime

import pytest
from django.urls import reverse

from applications.models import Application

get_url = reverse("application-list")
pytestmark = pytest.mark.django_db


@pytest.fixture
def create_application_record():
    application = Application.objects.create(
        FIO="Иванов Иван Иванович",
        FIO_manager="Пров Петр Прович",
        name_of_division="Отдел продаж",
        current_post="Менеджер по продажам",
        personal_achievements="Увеличение объем продаж на 20% за последний год",
        motivational_letter="Желание развиваться и расти профессионально в вашей компании",
        work_experience=36,
        time_created=datetime.now(),
        approved=False,
        watched=False,
    )
    return application


# ---------- Test GET  ----------
def test_get_applications_should_return_empty_list(client) -> None:
    response = client.get(get_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_get_applications_should_return_not_empty_list(
    client, create_application_record
) -> None:
    response = client.get(get_url)
    content = json.loads(response.content)

    assert response.status_code == 200

    assert len(content) == 1
    assert content[0]["FIO"] == "Иванов Иван Иванович"


# ---------- Test POST  ----------
def test_create_offer_should_succeed(client):
    response = client.post(
        get_url,
        data={
            "FIO": "string",
            "FIO_manager": "string",
            "name_of_division": "string",
            "current_post": "string",
            "personal_achievements": "string",
            "motivational_letter": "string",
            "work_experience": 1,
            "time_created": "2023-12-24T10:45:48.068Z",
            "approved": False,
            "watched": False,
        },
    )

    assert response.status_code == 201
    assert Application.objects.all().count() == 1


# ---------- Test DELETE  ----------
def test_delete_offer_should_succeed(client, create_application_record):
    url = reverse("application-detail", kwargs={"pk": 1})

    response = client.delete(url)

    assert response.status_code == 204
    assert Application.objects.all().count() == 0
