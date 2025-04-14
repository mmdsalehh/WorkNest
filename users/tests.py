from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def setUp(self):
        """Set up reusable variables for tests."""
        self.User = get_user_model()
        self.valid_email = "normal@user.com"
        self.valid_password = "foo"

    def test_create_user(self):
        """Test creating a regular user."""
        user = self.User.objects.create_user(
            email=self.valid_email, password=self.valid_password
        )
        self.assertEqual(user.email, self.valid_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, self.User.Role.Job_Seeker)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
            self.User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin_user = self.User.objects.create_superuser(
            email="super@user.com", password=self.valid_password
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.role, self.User.Role.Admin)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="super@user.com", password=self.valid_password, is_superuser=False
            )
