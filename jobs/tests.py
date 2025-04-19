from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Job

User = get_user_model()


class JobCreateTestCase(TestCase):
    def setUp(self):
        self.job_data = {
            "title": "Software Engineer",
            "description": "Develop and maintain software applications.",
            "type": 1,
            "location": "New York",
            "company": "Tech Company",
            "salary": 120000.00,
        }
        self.job_create_url = reverse("jobs:create")
        self.login_data = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "2",
        }

    def _register_and_authenticate(self):
        response = self.client.post(reverse("accounts:register"), self.login_data)
        self.assertEqual(response.status_code, 201)
        token = response.data.get("token")
        self.assertIsNotNone(token, "Token not returned on registration")
        return {"HTTP_AUTHORIZATION": f"Token {token}"}

    def test_job_creation(self):
        """Test that a job can be created by an employer user."""
        headers = self._register_and_authenticate()
        response = self.client.post(self.job_create_url, self.job_data, **headers)
        self.assertEqual(response.status_code, 201)
        data = response.data["data"]
        for field in ["title", "description", "type", "location", "company"]:
            self.assertEqual(data[field], self.job_data[field])
        self.assertEqual(float(data["salary"]), self.job_data["salary"])
        self.assertEqual(data["owner"], self.login_data["email"])


class JobListViewTest(TestCase):
    def setUp(self):
        self.job_list_url = reverse("jobs:list")
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword", role="2"
        )

        # Create some jobs for testing
        Job.objects.create(
            title="Software Engineer",
            description="Develop software",
            type=1,
            location="New York",
            company="Tech Inc.",
            owner=self.user,
            salary=120000.00,
        )
        Job.objects.create(
            title="Data Scientist",
            description="Analyze data",
            type=1,
            location="San Francisco",
            company="Data Corp.",
            owner=self.user,
            salary=150000.00,
        )
        Job.objects.create(
            title="Project Manager",
            description="Manage projects",
            type=1,
            location="Chicago",
            company="Project Co.",
            owner=self.user,
            salary=100000.00,
        )

    def test_job_list_data(self):
        """Test that the job list view returns the correct data."""
        response = self.client.get(self.job_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 3)

    def test_job_list_sorting_latest(self):
        """Test that the job list view sorts jobs by latest creation date."""
        response = self.client.get(self.job_list_url, {"sort": "latest"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jobs = response.data["data"]
        # Assuming the last created job is the first in the list
        self.assertEqual(jobs[0]["title"], "Project Manager")

    def test_job_list_sorting_earliest(self):
        """Test that the job list view sorts jobs by earliest creation date."""
        response = self.client.get(self.job_list_url, {"sort": "earliest"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jobs = response.data["data"]
        # Assuming the first created job is the first in the list
        self.assertEqual(jobs[0]["title"], "Software Engineer")

    def test_job_list_sorting_salary_highest(self):
        """Test that the job list view sorts jobs by highest salary."""
        response = self.client.get(self.job_list_url, {"sort": "salary_highest"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jobs = response.data["data"]
        self.assertEqual(jobs[0]["title"], "Data Scientist")

    def test_job_list_sorting_salary_lowest(self):
        """Test that the job list view sorts jobs by lowest salary."""
        response = self.client.get(self.job_list_url, {"sort": "salary_lowest"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jobs = response.data["data"]
        self.assertEqual(jobs[0]["title"], "Project Manager")

    def test_job_list_pagination(self):
        """Test that the job list view returns paginated results."""
        response = self.client.get(self.job_list_url, {"page": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pagination", response.data)

    def test_job_list_empty(self):
        """Test that the job list view returns an empty list when no jobs exist."""
        Job.objects.all().delete()  # Delete all jobs
        response = self.client.get(self.job_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 0)
