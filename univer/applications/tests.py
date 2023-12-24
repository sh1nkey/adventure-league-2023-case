import json
from datetime import datetime
from typing import List

import pytest
from django.urls import reverse

from applications.models import Application

companies_url = reverse("application-list")
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


# ---------- Test GET companies ----------
def test_get_applications_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_get_applications_should_return_not_empty_list(
    client, create_application_record
) -> None:
    response = client.get(companies_url)
    content = json.loads(response.content)

    assert response.status_code == 200

    assert len(content) == 1
    assert content[0]["FIO"] == "Иванов Иван Иванович"


