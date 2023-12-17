from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from applications.views import ApplicationViewSet
from univer.settings import DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

application_router = DefaultRouter()
application_router.register("", ApplicationViewSet, basename="application")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("application/", include(application_router.urls)),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/", include("users.urls")),
    path("content/", include("conent.urls")),
    path("timetable/", include("timetable.urls")),
]

if DEBUG:
    urlpatterns +=  [path('silk/', include('silk.urls', namespace='silk'))]