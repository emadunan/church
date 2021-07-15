from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Book, Chapter, Verse, Country

# APP VIEWS.
def view_index(request):
    return render(request, "scripture/index.html")


def view_guide(request):
    return render(request, "scripture/guide.html")


def view_login(request):
    if request.method == 'POST':
        pass

    else:
        return render(request, "scripture/login.html")


def view_register(request):
    countries = Country.objects.all().order_by('title')

    # Receive data from the post request and assign it into variables
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('e_mail')
        mobile = request.POST.get('mobile')
        country = request.POST.get('country')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # Validating received inputs
        if ((not username) or (not email) or (not first_name) or (not last_name) or (not password) or (not confirm)):
            return render(request, "scripture/register.html", {
                "countries": countries,
                "errorMessage": "برجاء ملئ كافة الحقول التى تنتهى بالعلامة (*) لانها ضرورية لانشاء الحساب"
            }) 

        print(username)
        return HttpResponse(username)

    else:
        return render(request, "scripture/register.html", {
            "countries": countries
        })


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

def view_search(request):
    if request.method == 'POST':
        criteria = request.POST.get('criteria')
        criteria = criteria.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')

        fields = [ request.POST.get('books'), request.POST.get('characters'), request.POST.get('blogs') ]
        print(fields)

        if criteria and 'books' in fields:
            verses = Verse.objects.filter(textq__contains=criteria)
        else:
            verses = None

        return render(request, "scripture/search.html", {
            "verses": verses,
            "search_criteria": criteria,
            "search_fields": fields
        })

    else:
        return render(request, "scripture/search.html")


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