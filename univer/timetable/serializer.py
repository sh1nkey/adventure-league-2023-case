from rest_framework import serializers


class SubjNameSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance


class StudentSurnameSerializer(serializers.Serializer):
    student__surname = serializers.CharField()
