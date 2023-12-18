from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)
    role = serializers.IntegerField(default=1)

    def validate_role(self, role):
        allowed_roles = [1, 2, 3, 4, 5]
        if not role in allowed_roles:
            raise serializers.ValidationError("Invalid role")

        return role
