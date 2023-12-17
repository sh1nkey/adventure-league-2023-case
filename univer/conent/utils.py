from django.db import transaction
from django.db.models import Q, Count, Case, When, BooleanField, Value
from django.http import JsonResponse

from conent.models import Tasks, Questions, TaskResult, Answer, Subjects, StudyMaterials
from conent.serializers import TaskResultSerializer
from users.models import StudentProfile


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
        subjects_data = (
            Subjects.objects
            .filter(tasks__in=Tasks.objects.filter(groups__students=user))
            .annotate(
                watched_materials=Count('studymaterials', filter=Q(studymaterials__who_watched=user)),
                total_materials=Count('studymaterials', distinct=True),
                done_tasks=Count('tasks', filter=Q(tasks__taskresult__student=user), distinct=True),
                total_tasks=Count('tasks', distinct=True)
            )
            .values('id', 'name', 'watched_materials', 'total_materials', 'done_tasks', 'total_tasks')
        )

        result = []

        for subject in subjects_data:
            success_percentage = round(
                (subject['watched_materials'] + subject['done_tasks'])
                / (subject['total_tasks'] + subject['total_materials']),
                1,
            )

            result.append(
                {
                    "subject_id": subject['id'],
                    "subject": subject['name'],
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
                    output_field=BooleanField()
                ),
                type=Value('test')
            )
            .order_by('done_or_not')
            .values('id', 'type', 'name', 'done_or_not')
            .distinct()
        )

        study_materials = (
            StudyMaterials.objects
            .prefetch_related("who_watched")
            .filter(subject_id=subject_id, group=student_group)
            .annotate(
                done_or_not=Case(
                    When(who_watched=user, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                ),
                type=Value('study_material')
            )
            .order_by('done_or_not')
            .values('id', 'type', 'name', 'done_or_not')
        )

        list_to_send = list(tasks) + list(study_materials)
        list_to_send.sort(key=lambda x: x['done_or_not'])

        return JsonResponse(list_to_send, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
