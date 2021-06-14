from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Book, Chapter, Verse

# APP VIEWS.
def view_index(request):
    return render(request, "scripture/index.html")


def view_books(request):
    books = Book.objects.all()
    return render(request, "scripture/books.html", {
        "books": books
    })


def view_book(request, id):
    book = Book.objects.get(pk=id)

    return render(request, "scripture/book.html", {
        "book": book,
        "chapters": book.chapter_set.all()
    })

def view_characters(request):
    return render(request, "scripture/characters.html")


def view_character(request, id):
    return render(request, "scripture/character.html")


def view_places(request):
    return render(request, "scripture/places.html")


def view_place(request, id):
    return render(request, "scripture/place.html")


def view_blogs(request):
    return render(request, "scripture/blogs.html")


def view_blog(request, id):
    return render(request, "scripture/blog.html")