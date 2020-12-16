from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelsTest(TestCase):

	def test_create_user_with_email_successfull(self):
		""" test create user models with email"""

		email = "pt@gmail.com"
		password = "pt123"
		user = get_user_model().objects.create_user(email=email, password=password)

		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))


	def test_new_user_email_normalization(self):
		email="pt@GMAIL.com"

		user = get_user_model().objects.create_user(email=email, password="test123")

		self.assertEqual(user.email, email.lower())

	def test_new_user_invalid_email(self):
		""" check user email"""

		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None,"pppppp")

	def test_create_superuser(self):
		""" create superuser and verify that """
		user = get_user_model().objects.create_superuser(
			email= "pt@gmail.com",
			password = "test123" 
			)
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)

