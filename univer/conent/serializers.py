from rest_framework import serializers
from rest_framework.serializers import ListSerializer

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


class SingleTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    subject__name = serializers.CharField()

class TasksSerializer(ListSerializer):
    child = SingleTaskSerializer()


class StudyMaterialSerializer(serializers.Serializer):
    name = serializers.CharField()
    subject = serializers.CharField()
    text = serializers.CharField()

class TaskMaterialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    done_or_not = serializers.BooleanField()

class TasksMaterialsSerializer(ListSerializer):
    child = TaskMaterialSerializer()