# Generated by Django 3.2.4 on 2021-07-24 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scripture', '0004_auto_20210710_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_verses',
            field=models.ManyToManyField(related_name='users_like', to='scripture.Verse'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='scripture.verse'),
        ),
    ]
