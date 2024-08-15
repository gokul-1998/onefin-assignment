from django.test import TestCase
from django.core.cache import cache
from ..middleware import RequestCounterMiddleware
from rest_framework import status
from django.contrib.auth.models import User


from rest_framework.test import APIClient

from django.test import TestCase
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RequestCounterMiddlewareTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        # self.middleware = RequestCounterMiddleware()
        cache.clear() 

    def test_request_count(self):
        # Perform requests
        response = self.client.get('/request-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        # Test if the request count is updated
        self.assertEqual(cache.get('request_count'), 1)

        # Perform another request to test if the count increments
        response = self.client.get('/request-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['requests'], 2)