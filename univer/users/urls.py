from django.urls import path

from .views import RegisterUser, ProfileGet

urlpatterns = [
    path("register", RegisterUser.as_view(), name="create-user"),
    path("profile", ProfileGet.as_view(), name="get-profile"),
]
