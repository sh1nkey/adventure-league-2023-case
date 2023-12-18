from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from applications.views import ApplicationViewSet
from univer.settings import DEBUG


application_router = DefaultRouter()
application_router.register("", ApplicationViewSet, basename="application")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("application/", include(application_router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/", include("users.urls")),
    path("content/", include("conent.urls")),
    path("timetable/", include("timetable.urls")),
]

if DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
