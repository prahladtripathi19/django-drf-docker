from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")

def create_user(**params):
	return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()

	def test_create_valid_user_success(self):
		""" Test to create a valid user public """
		payload = {
		"email":"test@gmail.com",
		"password":"test123",
		"name": "test"
		}
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(**res.data)
		self.assertTrue(user.check_password(payload["password"]))
		self.assertNotIn("password", res.data)
	def test_user_exist(self):
		""" Test for already exist user """
		payload = {
		"email":"test@gmail.com",
		"password":"test123",
		}
		create_user(**payload)
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_password_too_short(self):
		""" Test to check the password is too short """
		payload = {
		"email" : "test@gmail.com",
		"password":"pw",
		}
		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		user_exist = get_user_model().objects.filter(email=payload['email']).exists()
		self.assertFalse(user_exist)

	def test_create_token_for_user(self):
		""" Test to create token for user"""
		payload = {
		"email":"test@gmail.com",
		"password":"test123"
		}
		create_user(**payload)
		res = self.client.post(TOKEN_URL, payload)
		self.assertIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_create_token_for_invalid_credentials(self):
		""" Test that token is not created for invalid credentials """
		payload = {
		"email":"test@gmail.com",
		"password":"wrong"
		}
		create_user(email="test@gmail.com", password="test123")
		res = self.client.post(TOKEN_URL, payload)
		self.assertNotIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_token_no_user(self):
		""" Test token is not create is user not exist """
		payload = {
		"email":"test@gmail.com",
		"password":"wrong"
		}
		res = self.client.post(TOKEN_URL, payload)
		self.assertNotIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
	def test_create_token_missing_field(self):
		"""Test token is not create if any field is missing"""
		res = self.client.post(TOKEN_URL, {})
		self.assertNotIn("token", res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



