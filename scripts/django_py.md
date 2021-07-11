### Main Imports
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


### Script to update all verses
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
                vs = Verse.objects.get(number=idx+1, chapter=chapter)
                vs.text = verse.strip()
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


### Create new record for query purpose
from scripture.models import Verse
verses = Verse.objects.all()

for verse in verses:
    verse.textq = verse.text
    verse.save()
    print(verse.textq)


### Change (أ) or (إ) or (آ) with (ا), (ة) with (ه), (ى) with (ي)
from scripture.models import Verse
verses = Verse.objects.all()

for verse in verses:
    textt = ''
    for c in verse.textq:
        if c == 'أ':
            c = 'ا'
        elif c == 'إ':
            c = 'ا'
        elif c == 'آ':
            c = 'ا'
        elif c == 'ة':
            c = 'ه'
        elif c == 'ى':
            c = 'ي'
        else:
            c = c
        
        textt += c
    
    verse.textq = textt
    print(verse)
    print(verse.textq)
    verse.save()


### Read path in Django Shell
import os
from django.conf import settings

folder_path = os.path.join(settings.BASE_DIR, 'scripts')
print(folder_path)
    

### Read countries data from csv
import csv
import codecs
from scripture.models import Country

#### For Normal Characters
with open("D:\\.Sabbath\\church\\scripts\\countries1.csv", 'rU') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row[0], row[1], row[4], row[5])
        country = County(name=row[0], code=row[1], iso=row[4], title=row[5])
        county.save()

#### For Unicode Characters
csvReader = csv.reader(codecs.open('D:\\.Sabbath\\church\\scripts\\countries1.csv', 'rU', 'utf-16'))
for row in csvReader:
    print(row[0], row[1], row[2], row[3])
    country = Country(name=row[0], code=row[1], iso=row[2], title=row[3])
    country.save()

