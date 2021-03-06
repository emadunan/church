from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
    path('register', views.view_register, name='register'),
    path('login', views.view_login, name='login'),
    path('logout', views.view_logout, name='logout'),
    path('search', views.view_search, name='search'),
    path('guide', views.view_guide, name='guide'),
    path('mysettings', views.view_mysettings, name='mysettings'),
    path('retrieve-password', views.view_retrieve_password, name='retrieve-password'),
    path('reset-password', views.view_reset_password, name='reset-password'),
    path('verify', views.verify_new_user),
    path('userprofile', views.view_userprofile, name='userprofile'),
    

    path('books', views.view_books, name='books'),
    path('books/<int:id>', views.view_book, name='book'),

    path('characters', views.view_characters, name='characters'),
    path('characters/<int:id>', views.view_character, name='character'),

    path('places', views.view_places, name='places'),
    path('places/<int:id>', views.view_place, name='place'),

    path('blogs', views.view_blogs, name='blogs'),
    path('blogs/<int:id>', views.view_blog, name='blog'),
    path('blog-add', views.view_blog_add, name='blog-add'),
    path('blog-edit/<int:id>', views.view_blog_edit, name='blog-edit'),
    path('blog-del/<int:id>', views.view_blog_del, name='blog-del'),
    path('myblogs', views.view_my_blogs, name='my-blogs'),
    path('filtered-blogs', views.view_filter_blogs, name='filtered-blogs'),

    # API End Points
    path('setLocation', views.view_setLocation, name='setLocation'),
    path('getUserState', views.view_getUserState, name='getUserState'),
    path('getCurrentLocation', views.view_getCurrentLocation, name='getCurrentLocation'),
    path('addVerseToFavorites', views.view_addVerseToFavorites, name='addVerseToFavorites'),
    path('getFavVersesIdForUser', views.view_getFavVersesIdForUser, name='getFavVersesIdForUser'),
    path('getFavVersesForUser', views.view_getFavVersesForUser, name='getFavVersesForUser'),
    path('removeVerseFromFav/<int:id>', views.view_removeVerseFromFav, name='removeVerseFromFav'),
]
