from django.db import transaction
from django.db.models import Q, F, Count, Case, When, BooleanField, Value, Subquery
from django.http import JsonResponse

from conent.models import Tasks, Questions, TaskResult, Answer, Subjects, StudyMaterials
from conent.serializers import TaskResultSerializer
from timetable.serializer import StudentSurnameSerializer
from users.models import StudentProfile, Group


def get_single_task(id):
    try:
        task = Tasks.objects.get(id=id)

        questions = list(
            Questions.objects.filter(task=task).values("text", "id").order_by("id")
        )

        task_info = {
            "name": task.name,
            "subject": task.subject.name,
            "questions": questions,
        }
        return JsonResponse(task_info, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def send_answers(data, user, task_id):
    try:
        task = Tasks.objects.get(id=task_id)

        questions = list(Questions.objects.filter(task=task).order_by("id"))

        """Заносит ответы пользователя в БД"""
        with transaction.atomic():
            answers = [
                Answer(
                    answer=data[i]["answer_data"],
                    student=user,
                    question=questions[i],
                )
                for i in range(len(data))
            ]
            list_of_created = Answer.objects.bulk_create(answers)

        quantity_of_questions = len(list_of_created)

        correctness = 0
        for question, created_question in zip(questions, list_of_created):
            if question.right_answer == created_question.answer:
                correctness += 1

        result = TaskResult.objects.create(
            task=task,
            student=user,
            correct_percentage=round(correctness / quantity_of_questions, 1),
        )

        serialized_data = TaskResultSerializer(result)
        return JsonResponse(serialized_data.data, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_subjects_progress(user):
    try:
        group = Group.objects.get(students=user)
        subjects_data = (
            Subjects.objects.filter(groups=group)
            .annotate(
                watched_materials=Count(
                    "studymaterials", filter=Q(studymaterials__who_watched=user)
                ),
                total_materials=Count("studymaterials", distinct=True),
                done_tasks=Count(
                    "tasks", filter=Q(tasks__taskresult__student=user), distinct=True
                ),
                total_tasks=Count("tasks", distinct=True),
            )
            .values(
                "id",
                "name",
                "watched_materials",
                "total_materials",
                "done_tasks",
                "total_tasks",
            )
        )

        result = []

        for subject in subjects_data:
            success_percentage = round(
                (subject["watched_materials"] + subject["done_tasks"])
                / (subject["total_tasks"] + subject["total_materials"]),
                1,
            )

            result.append(
                {
                    "subject_id": subject["id"],
                    "subject": subject["name"],
                    "succeed_percentage": success_percentage,
                }
            )

        return JsonResponse(result, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def sub_task_material_get(user, subject_id):
    try:
        student_profile = StudentProfile.objects.prefetch_related("group").get(
            user=user
        )
        student_group = student_profile.group

        tasks = (
            Tasks.objects
            .prefetch_related("taskresult_set")
            .filter(subject_id=subject_id, groups=student_group)
            .annotate(
                done_or_not=Case(
                    When(taskresult__isnull=False, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                type=Value("test"),
            )
            .order_by("done_or_not")
            .values("id", "type", "name", "done_or_not")
            .distinct()
        )

        materials_done = (
            StudyMaterials.objects.prefetch_related("who_watched")
            .filter(subject_id=subject_id, who_watched=user)
            .annotate(done_or_not=Value(True), type=Value("study_material"))
            .values("id", "name", "type", "done_or_not")
        )

        list_of_done = (i["id"] for i in materials_done)
        materials_not_done = (
            StudyMaterials.objects.filter(
                subject_id=subject_id,
                group=student_group,
            )
            .exclude(id__in=list_of_done)
            .annotate(done_or_not=Value(False), type=Value("study_material"))
            .values("id", "name", "type", "done_or_not")
        )

        list_to_send = list(tasks) + list(materials_not_done) + list(materials_done)
        list_to_send.sort(key=lambda x: x["done_or_not"])

        return JsonResponse(list_to_send, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def watch_material(user, material_id):
    try:
        material = (
            StudyMaterials.objects.filter(id=material_id)
            .annotate(
                watched=Case(
                    When(who_watched=user, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                subject_name=F("subject__name"),
            )
            .first()
        )

        if not material.watched:
            material.who_watched.add(user)
            material.save()

        send_data = {
            "name": material.name,
            "subject": material.subject_name,
            "text": material.text,
        }

        return JsonResponse(send_data, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_tasks(user):
    try:
        user_profile = StudentProfile.objects.select_related("group").get(user=user)

        tasks_with_results = TaskResult.objects.values("task_id").distinct()

        """Получает невыполненный задачи у группы"""
        queryset = list(
            Tasks.objects.filter(groups=user_profile.group)
            .select_related("subject__name")
            .exclude(id__in=Subquery(tasks_with_results))
            .values("id", "name", "subject__name")
        )

        return JsonResponse(queryset, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def marking_visitors(data):
    try:
        serializer = StudentSurnameSerializer(data=data, many=True)
        if serializer.is_valid():
            students = StudentProfile.objects.filter(
                user__surname__in=[student["student__surname"] for student in data]
            )

            students.update(quantity_of_visiting=F("quantity_of_visiting") + 1)
            return JsonResponse(
                {"result": f"Отмечено {students.count()} человек"}, status=201
            )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
