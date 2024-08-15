from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class MovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_movie_list(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
