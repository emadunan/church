from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
    path('register', views.view_register, name='register'),
    path('login', views.view_login, name='login'),
    path('logout', views.view_logout, name='logout'),
    path('search', views.view_search, name='search'),
    path('guide', views.view_guide, name='guide'),

    path('books', views.view_books, name='books'),
    path('books/<int:id>', views.view_book, name='book'),

    path('characters', views.view_characters, name='characters'),
    path('characters/<int:id>', views.view_character, name='character'),

    path('places', views.view_places, name='places'),
    path('places/<int:id>', views.view_place, name='place'),

    path('blogs', views.view_blogs, name='blogs'),
    path('blogs/<int:id>', views.view_blog, name='blog'),

    # API End Points
    path('setLocation', views.view_setLocation, name='setLocation'),
    path('getUserState', views.view_getUserState, name='getUserState'),
    path('getCurrentLocation', views.view_getCurrentLocation, name='getCurrentLocation')
]
