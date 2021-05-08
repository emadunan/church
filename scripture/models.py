from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Scripture models.

class User(AbstractUser):
    pass


class Book(models.Model):
    number = models.IntegerField()
    symbol = models.CharField(max_length=3)
    title = models.CharField(max_length=33)
    titlelong = models.CharField(max_length=55)
    chapters = models.ForeignKey('Chapter', on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.number}) {self.title}"


class Chapter(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=55)
    verses = models.ForeignKey('Verse', on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.number}) {self.title}"


class Verse(models.Model):
    number = models.IntegerField()
    text = models.TextField()
    textf = models.TextField()

    def __str__(self):
        return f"({self.number}) {self.textf}"
