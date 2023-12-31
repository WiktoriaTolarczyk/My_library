# Generated by Django 4.2.4 on 2023-09-02 10:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biblioteka', '0002_mybook_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BooksToBuy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=128)),
                ('publisher', models.CharField(max_length=128)),
                ('update_date', models.DateField()),
                ('empik_price', models.FloatField()),
                ('tania_ksiazka_price', models.FloatField()),
                ('swiat_ksiazki_price', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(default=datetime.datetime(2023, 9, 2, 12, 33, 22, 766170))),
                ('plan_return_date', models.DateField()),
                ('real_return_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=64)),
                ('details', models.TextField()),
                ('goal', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='mybook',
            name='date_of_buy',
            field=models.DateField(default=datetime.datetime(2023, 9, 2, 12, 33, 22, 765299)),
        ),
        migrations.AddField(
            model_name='readingplan',
            name='books',
            field=models.ManyToManyField(related_name='books', to='biblioteka.mybook'),
        ),
        migrations.AddField(
            model_name='librarybooks',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteka.mybook'),
        ),
        migrations.AddField(
            model_name='library',
            name='books',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteka.librarybooks'),
        ),
    ]
