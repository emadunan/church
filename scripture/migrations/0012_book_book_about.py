# Generated by Django 3.2.4 on 2021-10-29 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripture', '0011_alter_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_about',
            field=models.TextField(null=True),
        ),
    ]
