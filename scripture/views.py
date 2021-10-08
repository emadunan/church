from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Blog, Book, Chapter, User, Verse, Country
from django.views.decorators.csrf import csrf_exempt
import json
import functools
import datetime
import string
import random
import smtplib
import jwt


# APP VIEWS.
def view_index(request):
    books = Book.objects.all()
    return render(request, "scripture/index.html", {
        "books": books
    })


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
        birthdate = request.POST.get('birthdate')
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
            birthdate=birthdate,
            is_active=False,
            password=make_password(password),
            gender=sex
        )
        user.save()

        # Creating access jwt token
        encoded_jwt = jwt.encode({"id": user.id, "email": user.email, "mobile":user.mobile}, "THE LORD IS MY PROVIDER", algorithm="HS256")

        # Sending the activation link by mail
        gmail_user = 'appmsr7@gmail.com'
        gmail_password = '4get@web'

        # try:
        to = [user.email]
        print(to)
        subject = 'Super Important Message'
        body = f'open the link to activate your account: http://127.0.0.1:8000/verify?t={encoded_jwt}'

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (gmail_user, ", ".join(to), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text)
        server.close()
        print('MAIL SENT!')


        # Login registered user and redirect him to the index page
        return render(request, "scripture/shortMessage.html", {
        "shortMessage": f"تم إنشاء الحساب، برجاء الدخول على البريد الإلكتروني الذ تم التسجيل به ({user.email}) والضغط على الرابط بالرسالة الوردة من فريق إدارة الموقع (appmsr7@gmail.com) لتفعيل الحساب، ثم الدخول بأستخدام أسم المستخدم وكلمة المرور الخاصة بكم."
    })

    else:
        return render(request, "scripture/register.html", {
            "countries": countries
        })


def verify_new_user(request):
    encoded_jwt = request.GET.get('t')
    decoded_jwt = jwt.decode(encoded_jwt, "THE LORD IS MY PROVIDER", algorithms=["HS256"])
    user = User.objects.get(pk=decoded_jwt['id'])
    user.is_active = True
    user.save()

    return HttpResponseRedirect(reverse('login'))
        

def view_reset_password(request):
    if request.method == 'POST':
        # Extracting data from the request
        oldPassword = request.POST.get("old_password")
        newPassword = request.POST.get("new_password")
        confirmPassword = request.POST.get("confirm_password")

        # Getting old password from db
        c_user = request.user
        user_old_password = c_user.password

        # Hashing the old password received in the request
        matchcheck = check_password(oldPassword, user_old_password)

        # Validating the old and new passwords
        if matchcheck and (newPassword == confirmPassword):
            print(newPassword)
            c_user.password = make_password(newPassword)
            c_user.save()
            return(HttpResponseRedirect(reverse('index')))

        print('password not match')
        return render(request, "scripture/resetPassword.html", {"errorMessage": "رجاء التأكد من صحة البيانات المدخلة، وإعادة المحاولة"})

    else:
        return render(request, "scripture/resetPassword.html")


def view_retrieve_password(request):
    if request.method == 'POST':
        user_username = request.POST.get('username')
        user_email = request.POST.get('email')
        user_mobile = request.POST.get('mobile')
        # get random password pf length 8 with letters, digits, and symbols
        # characters = string.ascii_letters + string.digits + string.punctuation
        characters = string.ascii_letters + string.digits
        temp_password = ''.join(random.choice(characters) for i in range(8))
        print(temp_password)

        # Save the temp password in the db
        user = User.objects.filter(email=user_email).first()
        
        if not user:
            return render(request, "scripture/retrievepassword.html", {
                "errorMessage": "رجاء التأكد من صحة البيانات المدخلة، وإعادة المحاولة"
            })
        
        if user_username == user.username and user_mobile == user.mobile:
            user.password = make_password(temp_password)
            user.save()
        else:
            return render(request, "scripture/retrievepassword.html", {
                "errorMessage": "رجاء التأكد من صحة البيانات المدخلة، وإعادة المحاولة"
            })

        # Send Mail to reset passwords
        gmail_user = 'appmsr7@gmail.com'
        gmail_password = '4get@web'

        # try:
        to = [user_email]
        subject = 'Super Important Message'
        # body = u'كلمة المرور المؤقتة هي: ({temp_password}) \n برجاء إعادة تعيين كلمة المرور بعد الدخول على الحساب، شكراً!'
        body = f'Your temp password: {temp_password}'

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (gmail_user, ", ".join(to), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text)
        server.close()
        print('MAIL SENT!')

        # except:
        #     print('Something went wrong...')

        return HttpResponseRedirect(reverse('retrieve-password'))

    else:
        return render(request, "scripture/retrievepassword.html")


def view_userprofile(request):
    return render(request, "scripture/userprofile.html")


def view_mysettings(request):
    return render(request, "scripture/mysettings.html")


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

def view_my_blogs(request):
    blogs = Blog.objects.filter(written_by=request.user)
    return render(request, "scripture/myblogs.html", {
        "blogs": blogs
    })


def view_filter_blogs(request):
    filtered_blogs = Blog.objects.filter(for_publish=True)

    if request.POST.get('title'):
        print('hit: title')
        title = request.POST.get('title')
        filtered_blogs = filtered_blogs.filter(title__contains=title)

    if request.POST.get('content'):
        print('hit: content')
        content = request.POST.get('content')
        filtered_blogs = filtered_blogs.filter(content__contains=content)

    if request.POST.get('written_by'):
        print('hit: written_by')
        written_by = request.POST.get('written_by')
        filtered_blogs = filtered_blogs.filter(Q(written_by__first_name=written_by) | Q(written_by__last_name=written_by))
    
    if request.POST.get('start_date') and request.POST.get('end_date'):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        filtered_blogs = filtered_blogs.filter(last_edited__range=(start_date, end_date))

    if request.POST.get('start_date') and request.POST.get('end_date'):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        filtered_blogs = filtered_blogs.filter(last_edited__range=(start_date, end_date))
    elif request.POST.get('start_date'):
        start_date = request.POST.get('start_date')
        filtered_blogs = filtered_blogs.exclude(last_edited__lt=start_date)
    elif request.POST.get('end_date'):
        end_date = request.POST.get('end_date')
        filtered_blogs = filtered_blogs.exclude(last_edited__gt=end_date)

    print(filtered_blogs)

    return render(request, "scripture/blogs.html", {
        "blogs": filtered_blogs
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
