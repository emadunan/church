from django.contrib import admin
from .models import Book, Chapter, Verse

# Models Declarations in the admin site.
class BookAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "symbol", "title", "titlelong")

# Models Registered in the admin site.
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter)
admin.site.register(Verse)