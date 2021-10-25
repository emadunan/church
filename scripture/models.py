from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Scripture models.

class User(AbstractUser):
    country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)
    mobile = models.CharField(max_length=22, null=True)
    gender = models.CharField(max_length=7, null=True)
    birthdate = models.DateField(null=True)
    location = models.OneToOneField('Verse', null=True, on_delete=models.RESTRICT)
    fav_verses = models.ManyToManyField('Verse', related_name='users_like')


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)
    iso = models.CharField(max_length=3)
    title = models.CharField(max_length=100)


class Identity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    fullname = models.TextField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(969)])
    about = models.TextField()
    identity = models.ManyToManyField(Identity)
    is_writter = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.name}"


class BooKMeta(models.Model):
    written_from = models.DateField(auto_now=False, auto_now_add=False)
    written_to = models.DateField(auto_now=False, auto_now_add=False)
    written_in = models.CharField(max_length=255)
    written_by = models.ManyToManyField(Character)
    about = models.TextField(null=True)


class Book(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    symbol = models.CharField(max_length=3)
    title = models.CharField(max_length=33)
    titlelong = models.CharField(max_length=99)
    book_meta = models.OneToOneField(BooKMeta, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"({self.number}) {self.name}"


class Chapter(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=55)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.name} ({self.number})"


class Verse(models.Model):
    number = models.IntegerField()
    text = models.TextField()
    textf = models.TextField()
    textq = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.number}) {self.textf}"


class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    for_publish = models.BooleanField()
    reviewed = models.BooleanField()
    written_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_edited = models.DateTimeField(auto_now=True)
