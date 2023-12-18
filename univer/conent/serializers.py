from rest_framework import serializers

from conent.models import Tasks, TaskResult, StudyMaterials


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        exclude = ["id"]


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        exclude = ["id"]


class AnswerSerializer(serializers.Serializer):
    answer_data = serializers.ListField(child=serializers.CharField())


class StudyMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterials
        exclude = ["who_watched"]


class TasksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    subject__name = serializers.CharField()
