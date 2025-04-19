from django.test import TestCase
from django.urls import reverse


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
