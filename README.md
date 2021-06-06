# Church

## About the project
This project targets to create admin panel which moderators can insert through it the verses of the bible, also allowing edit it if it required in case any type of mistakes founded in spelling or any other.

### References
https://en.wikipedia.org/wiki/Chapters_and_verses_of_the_Bible


### cli Commands

sqlite> UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='table_name';
sqlite> DELETE FROM table_name;
sqlite> VACUUM;

### Imports
from scripture.models import Book, Chapter, Verse
import re
from scripture.epk_scripture.helpers import ar_numbers


### Script to add chapters
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
for n in range(1, 67):
    with open(f"books/{n}.txt", "r", encoding="utf8") as f:
        book_txt = f.read()
        chs = book_txt.split('+++')
        for (i, ch) in enumerate(chs):
            book = Book.objects.get(number=n)
            chapter = Chapter.objects.filter(book=book).get(number=i+1)
            verses = re.split(r'\d+', ch)
            for (idx, verse) in enumerate(verses[1:]):
                print (verse[:-1])
                vs = Verse(number=idx+1, textf=verse.strip(), chapter=chapter)
                vs.save()

### Check verses count
book = Book.objects.get(pk=1)
chapters = book.chapter_set.all()
total = 0
for (idx, chapter) in enumerate(chapters):
    versesCount = chapter.verse_set.count()
    print(f"{idx+1}-> {versesCount}")
    total += versesCount

print(total)