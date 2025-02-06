"""
Test module for django admin modifications.
"""
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):
    """Test for django admin site."""

    def setUp(self):
        """Log in the admin user before each test."""
        self.client = Client()
        # self.factory = RequestFactory()
        """Create a superuser and a regular user for testing."""
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testcase123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')

        res = self.client.get(url)
        print(f"Response status code: {res.status_code}")

        # Access the changelist from context data
        # changelist = res.context_data['cl'].queryset
        # self.assertIn(self.user, changelist)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
