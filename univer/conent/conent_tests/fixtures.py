import pytest

from conent.models import Subjects, Tasks, StudyMaterials
from users.models import User, Group, StudentProfile
from users.views import get_tokens_for_user


@pytest.fixture
def subject_create() -> Subjects:
    return Subjects.objects.create(name="Тестовый предмет")


@pytest.fixture
def group_create() -> Group:
    return Group.objects.create(name="Тестовая группа")


@pytest.fixture
def create_task_record(subject_create):
    task = Tasks.objects.create(name="Example Task", subject=subject_create)
    return task


@pytest.fixture
def log_in_user():
    user = User.objects.create(username="test_user", role=2)
    token = get_tokens_for_user(user)["access"]
    return {
        'user': user,
        'token': token
    }


@pytest.fixture
def create_many_task_records(subject_create) -> Tasks:
    Tasks.objects.create(name="Example Task 1", subject=subject_create)
    Tasks.objects.create(name="Example Task 2", subject=subject_create)
    return Tasks.objects.all()


@pytest.fixture
def create_study_material(subject_create, group_create) -> StudyMaterials:
    created_material = StudyMaterials.objects.create(
        group=group_create,
        subject=subject_create,
        name="Тестовая статья",
        text="Тестовый текст",
    )
    return created_material

@pytest.fixture
def create_task_and_study_material(log_in_user, subject_create, group_create):
    created_material = StudyMaterials.objects.create(
        group=group_create,
        subject=subject_create,
        name="Тестовая статья",
        text="Тестовый текст",
    )
    created_task = Tasks.objects.create(
        name="Example Task",
        subject=subject_create
    )

    users_profile = StudentProfile.objects.get(user=log_in_user['user'])
    users_profile.group = group_create
    users_profile.save()
    created_task.groups.set([group_create])
    return {
        'material': created_material,
        'task': created_task,
        'group': group_create,
        'subject': subject_create,
        'user': log_in_user['token']
    }
