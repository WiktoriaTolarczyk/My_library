# Generated by Django 4.2.4 on 2023-09-21 00:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteka', '0003_bookstobuy_library_librarybooks_readingplan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarybooks',
            name='borrow_date',
            field=models.DateField(default=datetime.datetime(2023, 9, 21, 2, 4, 52, 389519)),
        ),
        migrations.AlterField(
            model_name='mybook',
            name='date_of_buy',
            field=models.DateField(default=datetime.datetime(2023, 9, 21, 2, 4, 52, 389129)),
        ),
    ]
