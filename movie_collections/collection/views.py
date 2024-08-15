from django.http import JsonResponse
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render

# Create your views here.
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.movie_api import get_movies
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Collection, Movie
from .serializers import CollectionSerializer, MovieSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class MovieListView(APIView):
    def get(self, request):
        page = request.query_params.get('page', 1)
        try:
            data = get_movies(page)
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionListCreateView(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.save(user=request.user)

        # Return the UUID in the response
        return Response(
            {"collection_uuid": collection.uuid},
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)

        # Generate list of collections with required fields
        collections_data = [
            {
                "title": collection["title"],
                "uuid": collection["uuid"],
                "description": collection.get("description", "")
            }
            for collection in serializer.data
        ]

        favourite_genres = self.get_favourite_genres(queryset)

        response_data = {
            "is_success": True,
            "data": {
                "collections": collections_data,
                "favourite_genres": favourite_genres
            }
        }

        return Response(response_data)

    def get_favourite_genres(self, queryset):

        genres_counter = {}
        for collection in queryset:
            for movie in collection.movies.all():
                for genre in movie.genres.all():
                    genres_counter[genre.name] = genres_counter.get(
                        genre.name, 0) + 1

        sorted_genres = sorted(
            genres_counter, key=genres_counter.get, reverse=True)
        return ", ".join(sorted_genres[:3])


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        uuid = self.kwargs.get('uuid')
        print("aaaaaa", uuid)

        obj = get_object_or_404(queryset, uuid=uuid)
        self.check_object_permissions(self.request, obj)
        return obj


class CollectionMoviesView(generics.RetrieveAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return Movie.objects.filter(collection__uuid=uuid)


class RequestCountView:
    REQUEST_COUNT_KEY = 'request_count'

    @staticmethod
    def get_request_count(request):
        count = cache.get(RequestCountView.REQUEST_COUNT_KEY, 0)
        return JsonResponse({"requests": count})

    @csrf_exempt
    @staticmethod
    def reset_request_count(request):
        if cache.get(RequestCountView.REQUEST_COUNT_KEY):
            cache.set(RequestCountView.REQUEST_COUNT_KEY, 0)
        else:
            cache.set(RequestCountView.REQUEST_COUNT_KEY, 0)
        return JsonResponse({"message": "request count reset successfully"})


class UserRegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate token manually after user creation
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'access_token': access_token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
