from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status

from applications.models import Application
from applications.serializers import ApplicationSerializer
from rest_framework.response import Response


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    @extend_schema(summary="Cоздаёт заявление")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
