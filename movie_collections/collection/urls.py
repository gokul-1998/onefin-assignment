from django.urls import path
from .views import MovieListView, UserRegistrationView
from django.urls import path
from .views import CollectionListCreateView, CollectionDetailView, CollectionMoviesView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('collection/', CollectionListCreateView.as_view(),
         name='collection-list-create'),
    path('collection/<uuid:uuid>/',
         CollectionDetailView.as_view(), name='collection-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),

]
