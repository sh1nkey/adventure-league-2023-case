from datetime import datetime

from django.db.models import Case, When, Value, BooleanField
from django.http import JsonResponse

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from conent.models import Tasks, StudyMaterials
from timetable.models import Day
from users.models import User, StudentProfile
from users.serializers import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from users.utils import profile_data


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterUser(CreateAPIView):
    """
    Касаемо ролей, там будет выбор между четырьмя:
    1 - абитуриент
    2 - студент
    3 - куратор
    4 - преподаватель
    5 - приёмная комиссия
    """

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.create(**self.request.data)
            user.set_password(self.request.data.get("password"))
            user.save()

            return JsonResponse(get_tokens_for_user(user), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class ProfileGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return profile_data(self.request.user)
