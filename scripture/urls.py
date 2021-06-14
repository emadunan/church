from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_index, name='main'),
    path('books', views.view_books, name='books'),
    path('books/<int:id>', views.view_book, name='book'),

    path('characters', views.view_characters, name='characters'),
    path('characters/<int:id>', views.view_character, name='character'),

    path('places', views.view_places, name='places'),
    path('places/<int:id>', views.view_place, name='place'),

    path('blogs', views.view_blogs, name='blogs'),
    path('blogs/<int:id>', views.view_blog, name='blog')
]
