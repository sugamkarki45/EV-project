from django.test import TestCase
from rest_framework.test import APIClient
from .models import User

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_request_otp(self):
        response = self.client.post('/api/v1/auth/request-otp/', {'phone': '9841234567'})
        self.assertEqual(response.status_code, 200)

    def test_verify_otp(self):
        response = self.client.post('/api/v1/auth/verify-otp/', {'phone': '9841234567', 'otp': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertEqual(User.objects.count(), 1)
