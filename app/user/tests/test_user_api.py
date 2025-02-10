"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public features of the user API"""
    def setUp(self):
        self.clent = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        print(f"User creation test response: {res.status_code}")

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        create_user(**payload)
        res = self.clent.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"Error if email exist test: {res.status_code}")

    def test_password_too_short_error(self):
        """Test error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
        print(f"Password too short test: {res.status_code}")

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'user-pass-123'
        }

        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(f"Token generated for valid credentials: {res.status_code}")

    def test_create_token_bad_credentials(self):
        """Test error returned for invalid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'goodpass'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'badpass'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"Error for invalid credentials: {res.status_code}")

    def test_create_token_blank_password(self):
        """Test error returned for blank password."""
        payload = {
            'email': 'test@example.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"Error for blank password: {res.status_code}")

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        print(f"Authentication required test: {res.status_code}")


class PrivateUserApiTest(TestCase):
    """Test API features that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='examplepass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test profile retrieval for logged in user."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })
        print(f"Profile retrieval test: {res.status_code}")

    def test_post_me_not_allowed(self):
        "Test POST is not allowed for me endpoint."
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        print(f"Post request to 'me' denial test: {res.status_code}")

    def test_update_user_profile(self):
        "Test profile update for authenticated users."
        payload = {
            'name': 'Updated Name',
            'password': 'Password123'
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(f"Profile update for valid user test: {res.status_code}")
