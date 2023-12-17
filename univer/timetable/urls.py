from django.urls import path

from timetable.views import ShowTimetable, SubjectsGet, GroupGet, StudGet, MarkVisitors
from django.urls import path, register_converter


urlpatterns = [
    path("timetable", ShowTimetable.as_view(), name="get-timetable"),
    path("subj-get", SubjectsGet.as_view(), name="get-subj"),
    path("group-get", GroupGet.as_view(), name="get-group"),
    path("stud-get", StudGet.as_view(), name="get-stud"),
    path("mark-visitors", MarkVisitors.as_view(), name="mark-visitors"),
]
