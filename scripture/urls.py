from django.urls import path
from . import views

urlpatterns = [
    path('books', views.view_books, name="books"),
    path('books/<int:id>', views.view_book, name="book")
]
