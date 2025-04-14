from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class RegisterViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse("accounts:register")
        cls.user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "newuser@test.com",
            "password": "newpass123",
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.filter(email=self.user_data["email"])
        self.assertTrue(user.exists())
        self.assertEqual(user.first().role, 1)


class LoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("accounts:login")
        cls.email = "newuser@test.com"
        cls.password = "testpass123"
        cls.login_data = {"email": cls.email, "password": cls.password}
        User.objects.create_user(**cls.login_data)

    def test_user_login(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)


class ProfileViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("accounts:login")
        cls.profile_url = reverse("accounts:profile")
        cls.email = "newuser@test.com"
        cls.password = "testpass123"
        cls.login_data = {"email": cls.email, "password": cls.password}
        User.objects.create_user(**cls.login_data)

    def test_user_profile(self):
        login_response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        token = login_response.data["token"]
        profile_response = self.client.get(
            self.profile_url, headers={"Authorization": f"Token {token}"}
        )
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
