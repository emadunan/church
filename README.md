# Church

## About the project
This project targets to create admin panel which moderators can insert through it the verses of the bible, also allowing edit it if it required in case any type of mistakes founded in spelling or any other.

### References
https://en.wikipedia.org/wiki/Chapters_and_verses_of_the_Bible


### cli Commands

UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='scripture_verse';

### Script to add chapters
from scripture.models import Book, Chapter
from scripture.epk_scripture.helpers import ar_numbers

book = Book.objects.get(pk=66)
print(book)

for ar_number in ar_numbers[:22]:
    chapter = Chapter(number = ar_number[0], title = ar_number[2], book = book)
    chapter.save()


### Script to add verses
with open("file.txt", "r") as f:
    chapter = f.read()
    verses = re.split(r'\d+', text)
    for (idx, verse) in enumerate(verses[1:]):
        print (str(idx + 1) + "- " + verse + '\n')


### Script to add all verses
with open("books/1.txt", "r", encoding="utf8") as f:
    book_txt = f.read()
    chs = book_txt.split('+++')
    for (i, ch) in enumerate(chs):
        book = Book.objects.get(number=1)
        chapter = Chapter.objects.filter(book=book).get(number=i+1)
        verses = re.split(r'\d+', ch)
        for (idx, verse) in enumerate(verses[1:]):
            print (verse[:-1])
            vs = Verse(number=idx+1, textf=verse[:-1], chapter=chapter)
            vs.save()