from django import forms
from .models import User, STATUS, MyBook, SHOP
from datetime import datetime, timedelta



class AddBookForm(forms.Form):
    """Form used to get data to create MyBook object."""
    title = forms.CharField(label="Tytuł")
    author = forms.CharField(label="Autor")
    publisher = forms.CharField(label="Wydawnictwo")
    date_of_buy = forms.DateField(label="Data nabycia", initial=datetime.now())
    status = forms.ChoiceField(choices=STATUS, label="Etap czytania")
    rating = forms.FloatField(min_value=0.0, max_value=10.0, label="Ocena (0-10):")
    review = forms.CharField(widget=forms.Textarea, label="Recenzja", initial="To be add")

class LoginUserForm(forms.Form):
    """Form used to get data to login user."""
    username = forms.CharField(label="Podaj nazwę użytkownika", max_length=64)
    password = forms.CharField(label="Podaj haslo", max_length= 64, widget=forms.PasswordInput())

class AddUserForm(forms.Form):
    """Form used to get data to register user."""
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Podaj haslo", max_length=64, widget=forms.PasswordInput())
    rep_pass = forms.CharField(label="Podaj haslo", max_length=64, widget=forms.PasswordInput())
    name = forms.CharField(label="Imię")
    lastname = forms.CharField(label="Nazwisko")
    mail = forms.CharField(label="Email", max_length=64, widget=forms.EmailInput())

class AddLibBookForm(forms.Form):
    """Form used to get data to create MyBook, LibraryBooks, Library objects."""
    title = forms.CharField(label="Tytuł")
    author = forms.CharField(label="Autor")
    publisher = forms.CharField(label="Wydawnictwo")
    date_of_buy = forms.DateField(label="Data wypożyczenia", initial=datetime.now())
    status = forms.ChoiceField(choices=STATUS, label="Etap czytania")
    rating = forms.FloatField(min_value=0.0, max_value=10.0, label="Ocena (0-10):")
    review = forms.CharField(widget=forms.Textarea, label="Recenzja", initial="To be add")
    plan_return_date = forms.DateField(label="Data zwrotu", initial=datetime.now()+timedelta(days=30))
    lib_name = forms.CharField(label="Nazwa biblioteki")

class AddPlanForm(forms.Form):
    """Form used to create ReadingPlanA object."""
    plan_name = forms.CharField(label="Nazwa planu")
    description = forms.CharField(widget=forms.Textarea, label="Opis planu", initial="To be add")
    goal = forms.IntegerField(label="Cel")

class AddBookToBuy(forms.Form):
    """Form used to create BooksToBuy object."""
    title = forms.CharField(label="Tytuł")
    author = forms.CharField(label="Autor")
    publisher = forms.CharField(label="Wydawnictwo")
    update_date = forms.DateField(label="Data aktualizacji cen", initial=datetime.now())
    empik = forms.FloatField(label="Cena w Empiku")
    tania_ksiazka = forms.FloatField(label="Cena w Taniej książce")
    swiat_ksiazki = forms.FloatField(label="Cena w Świecie książki")

class ChooseShopForm(forms.Form):
    """Form used to choose the store where the book was purchased."""
    shop = forms.ChoiceField(label="Wybierz sklep", choices=SHOP)
    price = forms.FloatField(label="Podaj cenę")

class PostponeReturnForm(forms.Form):
    """Form used to postpone return date of borrowed books."""
    return_date = forms.DateField(label="Nowa data zwrotu", initial=datetime.now()+timedelta(days=30))