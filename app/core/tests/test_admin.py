"""
Test module for django admin modifications.
"""
from django.urls import reverse
from django.test import Client, TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site
from ..admin import UserAdmin 
from ..models import User


class AdminSiteTests(TestCase):
    """Test for django admin site."""
       
    def setUp(self):
        """Log in the admin user before each test."""
        # self.client = Client()
        # self.client.force_login(self.admin_user)
        self.factory = RequestFactory()
        """Create a superuser and a regular user for testing."""
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testcase123',
            name='TestUser'
        )

    def test_users_list(self):
        """Test that users are listed on page."""

        # Create a mock GET request
        request = self.factory.get('/admin/core/user/')
        request.user = self.admin_user  # Set the user to the admin user

        admin_view = UserAdmin(User, site)
        res = admin_view.changelist_view(request)
        print(f"Response status code: {res.status_code}")

        # Access the changelist from context data
        changelist = res.context_data['cl'].queryset
        self.assertIn(self.user, changelist) 