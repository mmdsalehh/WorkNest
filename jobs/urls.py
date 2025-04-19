from django.urls import path

from .views import JobCreateView, JobListView

app_name = "jobs"

urlpatterns = [
    path("create/", JobCreateView.as_view(), name="create"),
    path("list/", JobListView.as_view(), name="list"),
]
