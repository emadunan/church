from django.contrib import admin
from .models import Book, Chapter, Verse

# Models Registered in the admin site.
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Verse)