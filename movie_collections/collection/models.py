import uuid
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "uuid": self.uuid,
            "movies": [movie.serialize() for movie in self.movies.all()]
        }


class Movie(models.Model):
    collection = models.ForeignKey(
        Collection, related_name='movies', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "genres": [genre.name for genre in self.genres.all()],
            "uuid": self.uuid,
            "collection_uuid": self.collection.uuid
        }

    def set_genres_from_string(self, genres_str):
        genre_names = [name.strip() for name in genres_str.split(',')]
        genres = [Genre.objects.get_or_create(
            name=name)[0] for name in genre_names]
        self.genres.set(genres)
