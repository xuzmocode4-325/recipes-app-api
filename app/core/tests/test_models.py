"""
Module for testing any models within the core app. 
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """
    Class for testing models. 
    """

    def test_create_user_with_email_success(self):
        """
        Test for successful creation of user with email address. 
        """
        email = 'test@example.com'
        password = 'test@123'
        user = get_user_model().objects.create_user(
            email, 
            password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))