from django.db.models import F
from django.http import JsonResponse

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from conent.models import Subjects
from conent.utils import marking_visitors
from timetable.serializer import SubjNameSerializer, StudentSurnameSerializer
from timetable.utils import get_timetable
from users.models import StudentProfile


class ShowTimetable(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "if_even", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            user_profile = StudentProfile.objects.get(user=self.request.user)
            if_even = True if self.request.query_params.get("if_even") == 'true' else False

            return JsonResponse(get_timetable(user_profile, if_even), safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class SubjectsGet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjNameSerializer
    queryset = Subjects.objects.all().values("name").order_by("name")


class GroupGet(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "subj_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            subj_name = self.request.query_params.get("subj_name")

            sending_data = list(
                Subjects.objects.filter(name=subj_name).values("groups__name")
            )

            return JsonResponse(sending_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



class StudGet(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "group_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            group_name = self.request.query_params.get("group_name")

            user_profile = list(
                StudentProfile.objects.filter(group__name=group_name)
                .values("user__surname", "user__name", "user__patronymic")
                .order_by("user__surname")
            )

            return JsonResponse(user_profile, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=400)


class MarkVisitors(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjNameSerializer(many=True)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"student__surname": openapi.Schema(type=openapi.TYPE_STRING)},
        )
    )
    def post(self, request, *args, **kwargs):
        return marking_visitors(request.data)

