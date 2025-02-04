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

    def test_new_user_email_mormalized(self):
        """
        Test email mormalization for new users.
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
            ['Test4@Example.Com', 'Test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
