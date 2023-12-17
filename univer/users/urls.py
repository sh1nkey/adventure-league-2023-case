from django.urls import path

from .views import RegisterUser, LogoutUser, ProfileGet

urlpatterns = [
    path("register", RegisterUser.as_view(), name="create-user"),
    path("logout", LogoutUser.as_view(), name="logout-user"),
    path("profile", ProfileGet.as_view(), name="get-profile"),
]
