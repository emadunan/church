from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Blog, Book, Chapter, User, Verse, Country
from django.views.decorators.csrf import csrf_exempt
import json
import functools
import datetime;


# APP VIEWS.
def view_index(request):
    return render(request, "scripture/index.html")


def view_main(request):
    return render(request, "scripture/main.html")

def view_guide(request):
    return render(request, "scripture/guide.html")


def view_login(request):
    if request.method == 'POST':
        # Login the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("blogs"))
        else:
            return render(request, "scripture/login.html", {
                "errorMessage": "رجاء التأكد من أسم المستخدم وكلمة المرور، وإعاده المحاولة"
            })

    else:
        return render(request, "scripture/login.html")


def view_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def view_register(request):
    countries = Country.objects.all().order_by('title')

    # Receive data from the post request and assign it into variables
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('e_mail')
        mobile = request.POST.get('mobile')
        country_id = request.POST.get('country')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        sex = request.POST.get('sex')

        # Validating received inputs
        if ((not username) or (not email) or (not first_name) or (not last_name) or (not password) or (not confirm)):
            return render(request, "scripture/register.html", {
                "countries": countries,
                "errorMessage": "برجاء ملئ كافة الحقول التى تنتهى بالعلامة (*) لانها ضرورية لانشاء الحساب"
            })

        registered_users = User.objects.filter(
            Q(username=username) | Q(email=email) | Q(mobile=mobile)).count()
        print("The Total count", registered_users)
        if registered_users > 0:
            return render(request, "scripture/register.html", {
                "countries": countries,
                "errorMessage": "هذا المستخدم مسجل بالفعل، من فضلك أستخدام (أسم - بريد - موبيل) أخر!"
            })

        if (password != confirm):
            return render(request, "scripture/register.html", {
                "countries": countries,
                "errorMessage": "رجاء التأكد من توافق كلمة المرور مع حقل التاكيد!"
            })

        # Register New User
        country = Country.objects.get(id=country_id)

        user = User(
            username=username,
            email=email,
            country=country,
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
            gender=sex
        )
        user.save()

        # Login registered user and redirect him to the index page
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

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
        criteria = criteria.replace('أ', 'ا').replace('إ', 'ا').replace(
            'آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')

        fields = [request.POST.get('books'), request.POST.get(
            'characters'), request.POST.get('blogs')]

        search_type = request.POST.get('searchType')

        # Searching in Books
        verses = ''
        if criteria and 'books' in fields and search_type == 'ANY':
            words = criteria.split(' ')
            verses = Verse.objects.filter(functools.reduce(lambda x, y: x | y, [Q(textq__contains=word) for word in words]))

        elif criteria and 'books' in fields and search_type == 'ALL':
            verses = Verse.objects.all()
            words = criteria.split(' ')
            for word in words:
                verses = verses.filter(textq__contains=word)

        elif criteria and 'books' in fields and search_type == 'FULL':
            verses = Verse.objects.filter(textq__contains=criteria)

        elif criteria and 'books' in fields and search_type == 'EXACT':
            verses = Verse.objects.filter(Q(textq__contains=f" {criteria} ") | Q(textq__contains=f" {criteria}.") | Q(
                textq__contains=f" {criteria}!") | Q(textq__contains=f" {criteria}?"))

        else:
            verses = None

        # Search in Characters  TODO

        # Search in Places TODO

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
    blogs = Blog.objects.all()

    return render(request, "scripture/blogs.html", {
        "blogs": blogs
    })


def view_blog(request, id):
    blog = Blog.objects.get(pk=id)
    return render(request, "scripture/blog.html", {
        "blog": blog
    })

def view_blog_add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        publish = request.POST.get('publish') == "PUB"

        blog = Blog(title=title, content=content, for_publish=publish, reviewed=True, written_by=request.user)
        blog.save()
        return HttpResponseRedirect(reverse('blogs'))

    else:
        return render(request, "scripture/blogadd.html")


def view_blog_edit(request, id):
    if request.method == "POST":
        # Receive the data from the request body
        title = request.POST.get('title')
        content = request.POST.get('content')
        publish = request.POST.get('publish') == "PUB"
        print(title, content, publish)

        # Get the targeted blog, and update it's values
        blog = Blog.objects.get(pk=id)
        blog.title = title
        blog.content = content
        blog.for_publish = publish
        blog.last_edited = datetime.datetime.now()

        blog.save()
        return HttpResponseRedirect(reverse('blogs'))
        # return HttpResponseRedirect(reverse('blog-edit', args=(id,)))

    else:
        selectedBlog = Blog.objects.get(pk=id)
        return render(request, 'scripture/blogedit.html', {
            "blog": selectedBlog
        })


def view_blog_del(request, id):
    blog = Blog.objects.get(pk=id)
    blog.delete()
    return HttpResponseRedirect(reverse('blogs'))




@login_required
@csrf_exempt
def view_setLocation(request):
    # Get the verse from request
    id = request.body
    verse = Verse.objects.get(id=int(id))

    # Get the logged user and update his location
    user = request.user
    user.location = verse
    user.save()
    return HttpResponse(id, status=200)


def view_getUserState(request):
    user = request.user

    return HttpResponse(json.dumps({
        'location': user.location.id
    }))


@login_required
def view_getCurrentLocation(request):
    user = request.user
    chapter = user.location.chapter
    book = chapter.book

    return HttpResponse(json.dumps({
        'vlocation': user.location.id,
        'chapter': chapter.id,
        'book': book.id
    }))


@login_required
@csrf_exempt
def view_addVerseToFavorites(request):
    user = request.user

    # Extract the verses id from the request's body
    response = json.loads(request.body)
    versesId = response['items']

    # Save the favorites in the Db
    for verseId in versesId:
        if verseId.isdigit():
            verse = Verse.objects.get(pk=int(verseId))
            user.fav_verses.add(verse)

    return HttpResponse(json.dumps({
        "items": response['items']
    }))


def view_getFavVersesIdForUser(request):
    user = request.user
    favVerses = user.fav_verses.all()

    # Extract verses' id and send them in the response
    items = []
    for verse in favVerses:
        print(verse)
        items.append(verse.id)

    return HttpResponse(json.dumps({
        "items": items
    }))


def view_getFavVersesForUser(request):
    user = request.user
    favVerses = user.fav_verses.all()

    return render(request, "scripture/favVerses.html", {
        "verses": favVerses
    })


def view_removeVerseFromFav(request, id):
    user = request.user
    verse = Verse.objects.get(pk=id)

    if (verse):
        user.fav_verses.remove(verse)

    return HttpResponseRedirect(reverse('getFavVersesForUser'))
