from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import MyBook, BooksToBuy, Library, LibraryBooks
from .forms import (
    AddBookForm,
    LoginUserForm,
    AddUserForm,
    AddLibBookForm,
)

# Create your views here.
class AddBookView(View):
    def get(self, request):
        form = AddBookForm()
        return render(request, 'add_book_form.html', {'form': form})
    def post(self, request):
        form = AddBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            publisher = form.cleaned_data['publisher']
            date_of_buy = form.cleaned_data['date_of_buy']
            status = form.cleaned_data['status']
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            user = User.objects.get(user=request.user)
            book = MyBook.objects.create(user=user,
                                         title=title,
                                         author=author,
                                         publisher=publisher,
                                         date_of_buy=date_of_buy,
                                         status=status,
                                         rating=rating,
                                         review=review)
            message = 'Gratulacje! książka została dodana! Możesz dodać następną.'
            ctx = {
                'message': message,
                'form': form,
            }
            return render(request, 'add_book_form.html', context=ctx)

class LoginUser(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'login_user.html', {'form': form})
    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                message = 'Udało się zalogować i uwierzytelnić! Witaj ' + request.user.username
                ctx = {
                    'message': message,
                    'form': form,
                }
                return render(request, 'login_user.html', context=ctx)
            else:
                message = 'Nie udało się uwierzytelnić więc nie można zalogować! :('
                ctx = {
                    'message': message,
                    'form': form,
                }
                return render(request, 'login_user.html', context=ctx)

class LogoutUser(View):
    def get(self, request):
        logout(request)
        message = 'Użytkownik wylogowany, zaloguj ponownie!'
        ctx = {
            'message': message,
        }
        return render(request, 'logout_user.html', context=ctx)


class AddUser(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            rep_password = form.cleaned_data['rep_pass']
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            mail = form.cleaned_data['mail']
            try:
                user = User.objects.get(username=login)
            except User.DoesNotExist:
                user = None
            if user is not None:
                mass = 'Login użytkownika istnieje już w bazie danych spróbuj ponownie'
                ctx = {
                    'message': mass,
                    'form': form,
                }
                return render(request, 'add_user.html', context=ctx)
            else:
                if password == rep_password:
                    user_stop = User.objects.create_user(username= login, first_name=name, last_name=lastname, email=mail, password=password )
                    mass = 'Użytkownik ' + login + ' został dodany!\n Możesz dodać następnego.'
                    ctx = {
                        'message': mass,
                        'form': form,
                    }
                    return render(request, 'add_user.html', context=ctx)
                else:
                    mass = 'Hasło się nie zgadza wypełnij dane ponownie!'
                    ctx = {
                        'message': mass,
                        'form': form,
                    }
                    return render(request, 'add_user.html', context=ctx)

class BookListView(View):
    def get(self, request):
        books = MyBook.objects.all().order_by('title')
        paginator = Paginator(books, 10)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        ctx = {
            'books': books,
            'i': 0,
        }
        return render(request, 'books-list.html', context=ctx)

class LandingPageView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class ShoppingListView(View):
    def get(self, request):
        books = BooksToBuy.objects.all().order_by('title')
        paginator = Paginator(books, 50)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        ctx = {
            'books': books,
            'i': 0,
        }
        return render(request, 'shop-list.html', context=ctx)
    
class LibraryListView(View):
    def get(self, request):
        library = Library.objects.all().order_by('lib_name')
        paginator = Paginator(library, 5)
        page = request.GET.get('page')
        library = paginator.get_page(page)
        ctx = {
            "libraries" : library,
        }
        return render(request, 'lib_list.html', context=ctx)
    
class AddLibBookView(View):
    def get(self, request):
        form = AddLibBookForm()
        return render(request, 'add_Libbook_form.html', {'form': form})
    def post(self, request):
        form = AddLibBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            publisher = form.cleaned_data['publisher']
            date_of_buy = form.cleaned_data['date_of_buy']
            status = form.cleaned_data['status']
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            user = User.objects.get(user=request.user)

            book = MyBook.objects.create(user=user,
                                         title=title,
                                         author=author,
                                         publisher=publisher,
                                         date_of_buy=date_of_buy,
                                         status=status,
                                         rating=rating,
                                         review=review)
            
            borrow_date = form.cleaned_data['date_of_buy']
            plan_return_date = form.cleaned_data['plan_return_date']

            libBook = LibraryBooks.objects.create(book=book,
                                                  borrow_date=borrow_date,
                                                  plan_return_date=plan_return_date)
            
            lib_name = form.cleaned_data['lib_name']
            
            try:
                library = Library.books.get(lib_name=lib_name)
            except library.DoesNotExist:
                library = None
            if library is not None:
                library.objects.add(libBook)
                mass = 'Biblioteka użytkownika istnieje już w bazie danych, obiekt został dodany'
                ctx = {
                    'message': mass,
                    'form': form,
                }
                return render(request, 'add_library.html', context=ctx)
            else:
                library = Library.objects.create(books=libBook, lib_name=lib_name)
            message = 'Gratulacje! Biblioteka została dodana! Możesz dodać następną.'
            ctx = {
                'message': message,
                'form': form,
            }
            return render(request, 'add_libary_form.html', context=ctx)
    
class RankingView(View):
    def get(self, request):
        return render(request, 'ranking.html')
    
class StatisticsView(View):
    def get(self, request):
        return render(request, 'statistics.html')