from rest_framework import serializers
from .models import Collection, Movie, Genre
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

    def to_internal_value(self, data):
        genres = data.get('genres', '')

        if isinstance(genres, str):
            genres_list = [genre.strip()
                           for genre in genres.split(',') if genre.strip()]
            data['genres'] = genres_list

        return super().to_internal_value(data)

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        movie = Movie.objects.create(**validated_data)

        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            movie.genres.add(genre)
        return movie

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if genres_data is not None:
            instance.genres.clear()
            for genre_name in genres_data:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                instance.genres.add(genre)

        return instance


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies', 'uuid']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)

        for movie_data in movies_data:
            movie_serializer = MovieSerializer(data=movie_data)
            if movie_serializer.is_valid():
                movie = movie_serializer.save(collection=collection)

        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if movies_data is not None:
            for movie_data in movies_data:
                movie_uuid = movie_data.get('uuid')
                if movie_uuid:
                    movie_instance = Movie.objects.get(uuid=movie_uuid)
                    movie_serializer = MovieSerializer(
                        movie_instance, data=movie_data)
                    if movie_serializer.is_valid():
                        movie_serializer.save()
                else:
                    movie = Movie.objects.create(
                        collection=instance, title=movie_data['title'], description=movie_data['description'])
                    genres_data = movie_data.get('genres', [])
                    if genres_data:
                        genres_list = [Genre.objects.get_or_create(
                            name=genre_name)[0] for genre_name in genres_data]
                        movie.genres.set(genres_list)

        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
