from django.contrib import admin
from .models import Book, Chapter, Verse, User, Character, BooKMeta

# Models Declarations in the admin site.
class BookAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "symbol", "title", "titlelong")

# Models Registered in the admin site.
admin.site.register(Book, BookAdmin)
admin.site.register(Character)
admin.site.register(BooKMeta)

admin.site.register(Chapter)
admin.site.register(Verse)
admin.site.register(User)