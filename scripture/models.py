from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Scripture models.

class User(AbstractUser):
    pass


class Character(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    fullname = models.TextField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(969)])
    about_me = models.TextField()
    is_writter = models.BooleanField()


class BooKMeta(models.Model):
    written_from = models.DateField(auto_now=False, auto_now_add=False)
    written_to = models.DateField(auto_now=False, auto_now_add=False)
    written_in = models.TextField()
    written_by = models.ManyToManyField(Character)


class Book(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    symbol = models.CharField(max_length=3)
    title = models.CharField(max_length=33)
    titlelong = models.CharField(max_length=99)
    book_meta = models.OneToOneField(BooKMeta, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"({self.number}) {self.name}"


class Chapter(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=55)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.number}) {self.title}"


class Verse(models.Model):
    number = models.IntegerField()
    text = models.TextField()
    textf = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.number}) {self.textf}"
