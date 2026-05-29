from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserViewTests(TestCase):
    def test_logout_requires_post(self):
        user = User.objects.create_user(username="user", password="StrongPass123!")
        self.client.force_login(user)

        response = self.client.get(reverse("user:logout"))

        self.assertEqual(response.status_code, 405)

    def test_logout_with_post_redirects_home(self):
        user = User.objects.create_user(username="user", password="StrongPass123!")
        self.client.force_login(user)

        response = self.client.post(reverse("user:logout"))

        self.assertRedirects(response, reverse("index"))
