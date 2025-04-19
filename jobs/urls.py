from django.urls import path

from .views import JobCreateView

app_name = "jobs"

urlpatterns = [
    path("create/", JobCreateView.as_view(), name="create"),
]
