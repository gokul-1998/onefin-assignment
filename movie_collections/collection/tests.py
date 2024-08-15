from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Collection, Movie, Genre
from django.contrib.auth.models import User
import uuid

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Collection, Movie, Genre
from django.contrib.auth.models import User
import uuid
from .test.test_middleware import RequestCounterMiddlewareTests

class MovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Comedy')
        
        self.collection = Collection.objects.create(user=self.user, title='My Collection', description='A great collection')
        self.movie = Movie.objects.create(
            collection=self.collection,
            title='My Movie',
            description='A great movie',
        )
        self.movie.genres.set([self.genre1, self.genre2])
        self.movie.save()
        
        self.movie_data = {
            'title': 'New Movie',
            'description': 'A new great movie',
            'genres': ['Drama', 'Horror']
        }

 

from rest_framework import status
from django.urls import reverse

class CollectionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.collection_data = {
            'title': 'New Collection',
            'description': 'A brand new collection',
        }

    def test_collection_list_create(self):
        response = self.client.get(reverse('collection-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.post(reverse('collection-list-create'), self.collection_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(Collection.objects.first().title, 'New Collection')

    def test_collection_detail(self):
        collection = Collection.objects.create(user=self.user, title='Collection Detail', description='Details')
        response = self.client.get(reverse('collection-detail', args=[collection.uuid]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Collection Detail')

    

class UserRegistrationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        user_data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post('/register/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'newuser')
