from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

STATUS = (
    (1, "Nieprzeczytana"),
    (2, "W trakcie czytania"),
    (3, "Przeczytana"),
)

MONTHS = [
    'Styczeń',
    'Luty',
    'Marzec',
    'Kwiecień',
    'Maj',
    'Czerwiec',
    'Lipiec',
    'Sierpień',
    'Wrzesień',
    'Październik',
    'Listopad',
    'Grudzień'
]

def get_author_rate(ratings, book_number, most_popular_book_num):
    return 0.6 * sum(ratings)/(len(ratings)*10) + 0.4*book_number/most_popular_book_num

# class User(models.Model):
#     name = models.CharField(max_length=128)
#     surname = models.CharField(max_length=128)
#     nick = models.CharField(max_length=128, unique=True)
#     password = models.TextField()

class MyBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    date_of_buy = models.DateField(default=datetime.now())
    status = models.IntegerField(choices=STATUS)
    rating = models.FloatField()
    review = models.TextField(null=True)

    @property
    def name(self):
        return "{}, {}".format(self.title, self.author)

    def __str__(self):
        return self.name


class LibraryBooks(models.Model):
    book = models.ForeignKey(MyBook, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=datetime.now())
    plan_return_date = models.DateField()
    real_return_date = models.DateField(null = True)


class Library(models.Model):
    books = models.ForeignKey(LibraryBooks, on_delete=models.CASCADE)
    lib_name = models.CharField(max_length=128)

    @property
    def name(self):
        return "{}".format(self.lib_name)

    def __str__(self):
        return self.name



class ReadingPlanA(models.Model):
    books = models.ManyToManyField(MyBook, through="PlanBooks", related_name='books')
    plan_name = models.CharField(max_length=64)
    details = models.TextField()
    goal = models.IntegerField(null = True)

    @property
    def name(self):
        return "{}".format(self.plan_name)

    def __str__(self):
        return self.name

class PlanBooks(models.Model):
    reading_plan = models.ForeignKey(ReadingPlanA ,on_delete=models.CASCADE)
    book = models.ForeignKey(MyBook,  on_delete=models.CASCADE)
    is_read = models.BooleanField()

    
class BooksToBuy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    update_date = models.DateField()
    empik_price = models.FloatField()
    tania_ksiazka_price = models.FloatField()
    swiat_ksiazki_price = models.FloatField()

    @property
    def name(self):
        return "{}, {}".format(self.title, self.author)

    def __str__(self):
        return self.name