# Church

## About the project
This project targets to create admin panel which moderators can insert through it the verses of the bible, also allowing edit it if it required in case any type of mistakes founded in spelling or any other.

### References
https://en.wikipedia.org/wiki/Chapters_and_verses_of_the_Bible


### cli Commands

UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='table_name';

from scripture.models import Book, Chapter
from scripture.epk_scripture.helpers import ar_numbers

book = Book.objects.get(pk=66)
print(book)

for ar_number in ar_numbers[:22]:
    chapter = Chapter(number = ar_number[0], title = ar_number[2], book = book)
    chapter.save()