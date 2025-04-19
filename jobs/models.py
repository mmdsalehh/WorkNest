from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Job(models.Model):
    class JobType(models.IntegerChoices):
        FULL_TIME = 1, "Full Time"
        PART_TIME = 2, "Part Time"
        CONTRACT = 3, "Contract"
        INTERNSHIP = 4, "Internship"
        TEMPORARY = 5, "Temporary"
        VOLUNTEER = 6, "Volunteer"

    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.IntegerField(
        choices=JobType.choices,
    )
    location = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"


class Application(models.Model):
    class Status(models.IntegerChoices):
        APPLIED = 1, "Applied"
        UNDER_REVIEW = 2, "Under Review"
        INTERVIEW = 3, "Interview"
        OFFERED = 4, "Offered"
        REJECTED = 5, "Rejected"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="resumes/")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.APPLIED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email} applied for {self.job.title}"

    class Meta:
        unique_together = ("job", "user")
        ordering = ["-applied_at"]
        verbose_name = "Application"
        verbose_name_plural = "Applications"
