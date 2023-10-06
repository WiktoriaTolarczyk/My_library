from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import MyBook, BooksToBuy, Library, LibraryBooks, MONTHS, ReadingPlanA, PlanBooks
from django.core.exceptions import ObjectDoesNotExist
from .forms import (
    AddBookForm,
    LoginUserForm,
    AddUserForm,
    AddLibBookForm,
    AddPlanForm,
    AddBookToBuy,
    ChooseShopForm,
    PostponeReturnForm,
    AddPricesForm,
)

# Create your views here.
class AddBookView(View):
    """View of form used to add book to database"""
    def get(self, request):
        """Function to handle add-book's request with get method"""
        form = AddBookForm()
        return render(request, 'add_book_form.html', {'form': form})
    def post(self, request):
        """Function to handle add-book's request with post method"""
        form = AddBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            publisher = form.cleaned_data['publisher']
            date_of_buy = form.cleaned_data['date_of_buy']
            status = form.cleaned_data['status']
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            user = User.objects.get(username=request.user.username)
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
    """View used to login user via appropriate form"""
    def get(self, request):
        """Function to handle login-user's request with get method"""
        form = LoginUserForm()
        return render(request, 'login_user.html', {'form': form})
    def post(self, request):
        """Function to handle login-user's request with post method"""
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
    """View used to logout logged user"""
    def get(self, request):
        """Function to handle logout-user's request with get method"""
        logout(request)
        message = 'Użytkownik wylogowany, zaloguj ponownie!'
        ctx = {
            'message': message,
        }
        return render(request, 'logout_user.html', context=ctx)


class AddUser(View):
    """View used to add user via model django.contrib.auth.models.User"""
    def get(self, request):
        """Function to handle add-user's request with get method"""
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})

    def post(self, request):
        """Function to handle add-user's request with post method"""
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
    """View used to display list of books added to database.
        Books presented here are created via MyBook model presented in models.py dedicated file."""
    def get(self, request):
        """Function to handle display-book-list's request with get method"""
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
    """View used to display landing page view."""
    def get(self, request):
        """Function to handle display-landing-page's request with get method"""
        return render(request, 'index.html')
    
class ShoppingListView(View):
    """View used to display list of books that the user wants to buy.
        Books presented here are created via BooksToBuy model presented in models.py dedicated file."""
    def get(self, request):
        """Function to handle display-books_to_buy-list's request with get method"""
        books = BooksToBuy.objects.filter(book_status=2).order_by('title').distinct('title')
        paginator = Paginator(books, 50)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        ctx = {
            'books': books,
            'i': 0,
        }
        return render(request, 'shop-list.html', context=ctx)
    
class LibraryListView(View):
    """View used to display list of books borrowed from libraries by the user cathegorized by libraries.
    Books presented here are created via LibraryBooks model presented in models.py dedicated file.
    Libraries (Library model) displayed via LibraryListView are connected to LibraryBooks by a one-to-many relation."""
    def get(self, request):
        """Function to handle display-books_from-libraries-list's request with get method"""
        library = Library.objects.all().order_by('lib_name').distinct('lib_name')
        books = Library.objects.all().order_by('lib_name')
        paginator = Paginator(library, 5)
        page = request.GET.get('page')
        library = paginator.get_page(page)
        ctx = {
            "libraries" : library,
            "books" : books,
        }
        return render(request, 'lib_list.html', context=ctx)
    
class AddLibBookView(View):
    """View used to add book to database.
    This book is borrowed from library so MyBook, LibraryBooks, Library models are used to create book object."""
    def get(self, request):
        """Function to handle add-library-book's request with get method"""
        form = AddLibBookForm()
        return render(request, 'add_Libbok_form.html', {'form': form})
    def post(self, request):
        """Function to handle add-library-book's request with post method"""
        form = AddLibBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            publisher = form.cleaned_data['publisher']
            date_of_buy = form.cleaned_data['date_of_buy']
            status = form.cleaned_data['status']
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            user = User.objects.get(username=request.user.username)

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


            library = Library.objects.filter(lib_name=lib_name)
            if not library:
                library = None
            else:
                library = library[0]
            if library is not None:
                library = Library.objects.create(books=libBook, lib_name=lib_name)
                mass = 'Biblioteka użytkownika istnieje już w bazie danych, obiekt został dodany'
                ctx = {
                    'message': mass,
                    'form': form,
                }
                return render(request, 'add_Libbok_form.html', context=ctx)
            else:
                library = Library.objects.create(books=libBook, lib_name=lib_name)
            message = 'Gratulacje! Biblioteka została dodana! Możesz dodać następną.'
            ctx = {
                'message': message,
                'form': form,
            }
            return render(request, 'add_Libbok_form.html', context=ctx)
    
class RankingView(View):
    """View dedicated to display books ranking; graphical visualization of the highest book ratings from database
    and also with list of them with highest rates"""
    def get(self, request):
        """Function to handle display-ranking's request with get method"""
        books = MyBook.objects.all().order_by('-rating')
        books_ = MyBook.objects.all().order_by('-rating')[:5]
        rating = []
        for book in books_:
            rating.append(float(str(book.rating).replace(',','.')))
        ratings = [i.rating for i in books_]
        paginator = Paginator(books, 10)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        ctx = {
            "books": books,
            "books_": books_,
            "ratings": ratings,
        }
        return render(request, 'rating.html', context=ctx)
    
class StatisticsView(View):
    """View dedicated to display reading statistics; graphical visualization of:
        -Dynamically updated histogram of the number of books read per year,
        -A chart showing data related to the most frequently chosen library,
        -A chart showing data related to the most frequently chosen author."""
    def get(self, request):
        """Function to handle display-statistics's request with get method"""
        books = MyBook.objects.filter(status=3)
        number = []
        for i in range(12):
            number += [books.filter(date_of_buy__month = i).count()]

        library = Library.objects.all().order_by('lib_name').distinct('lib_name')
        lib_names = []
        lib_counts = []
        for lib in library:
            lib_names += [lib.lib_name]
            lib_counts += [Library.objects.filter(lib_name = lib.lib_name).count()]

        authors = MyBook.objects.all().order_by('author').distinct('author')
        data = []
        list = []
        for i in range(len(authors)):
            data.append(MyBook.objects.filter(author = authors[i].author).count())
            list.append(i)
        author = []
        num = []
        for _ in range(5):
            author.append(authors[list[data.index(max(data))]].author)
            num.append(max(data))
            list.remove(list[data.index(max(data))])
            data.remove(max(data))
        indexes = []
        for k in range(5):
            indexes.append(k)
        ctx = {
            "number": number,
            "months": MONTHS,
            "lib_name": lib_names,
            "lib_count": lib_counts,
            "authors": author,
            "num_book": num,

        }
        return render(request, 'stat.html', context=ctx)

class ReadingPlanAddView(View):
    """View dedicated to add new reading plan. This object has its own dedicated model: ReadingPlanA presented
    in models.py file."""
    def get(self, request):
        """Function to handle add-reading-plan's request with get method"""
        form = AddPlanForm()
        return render(request, 'add_plan_form.html', {'form': form})
    def post(self, request):
        """Function to handle add-reading-plan's request with post method"""
        form = AddPlanForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['plan_name']
            description = form.cleaned_data['description']
            goal = form.cleaned_data['goal']
            plan = ReadingPlanA.objects.create(plan_name=name,
                                              details=description,
                                              goal=goal)
            return redirect('/plan/' + str(plan.id))

class AddBookToPlanView(View):
    """View used to add book to previously created reading plan.
        ReadingPlanA and MyBook models are connected with many-to-many relation via PlanBooks model."""
    def get(self, request):
        """Function to handle add-book-to-plan's request with get method"""
        plans = ReadingPlanA.objects.all()
        books = MyBook.objects.all()
        ctx = {
            'plans': plans,
            'books': books
        }
        return render(request, "add_book_to_plan.html", context=ctx)
    def post(self, request):
        """Function to handle add-book-to-plan's request with post method"""
        plan_name = request.POST.get("plan_name")
        book = request.POST.get("book")
        is_read = request.POST.get("book_read")

        if plan_name and book and is_read:
            plan = ReadingPlanA.objects.get(plan_name = plan_name)
            book = MyBook.objects.filter(title = book)[0]
            if is_read == 'True':
                is_read = True
            else:
                is_read = False
            PlanBooks.objects.create(reading_plan=plan, book=book, is_read=is_read)
            return redirect(f"/plan/{plan.pk}")
        else:
            message = 'Wypełnij poprawnie wszystkie pola'

        return render(request, "app-schedules-meal-recipe.html", {'message': message})

class ReadingPlanDetailView(View):
    """View intended to display details of the chosen reading plan."""
    def get(self, request, id):
        """Function to handle add-book-to-plan's request with get method

        Parameters:
        id (int): id number (from database) of chosen reading plan"""
        plans_count = ReadingPlanA.objects.count()
        if id in [i for i in range(1, plans_count + 1)]:
            plans = ReadingPlanA.objects.all()
            plan = plans[id - 1]
            read_books = PlanBooks.objects.filter(reading_plan = plan, is_read=True)
            books = []
            for i in range(len(read_books)):
                books.append(read_books[i].book)
            rest_books = PlanBooks.objects.filter(reading_plan = plan, is_read=False)
            bookss = []
            for i in range(len(rest_books)):
                bookss.append(rest_books[i].book)
            if PlanBooks.objects.filter(reading_plan = plan).count() != 0:
                num = int(read_books.count()/PlanBooks.objects.filter(reading_plan = plan).count() * 100)
            else:
                num = 0
            context = {
                'plan' : plan,
                'read_book' : books,
                'rest_book' : bookss,
                'all_books' : num,
                'percent': num

            }
            return render(request, "plan_details.html", context=context)

class AddBookToBuyView(View):
    """View used to add book to database. Book is not
        The book does not belong to the user yet, but the user intends to purchase it.
        It is created via BooksToBuy dedicated model."""
    def get(self, request):
        """Function to handle add-book-to-buy's request with get method"""
        form = AddBookToBuy()
        return render(request, 'add_book_to_buy_form.html', {'form': form})

    def post(self, request):
        """Function to handle add-book-to-buy's request with post method"""
        form = AddBookToBuy(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            publisher = form.cleaned_data['publisher']
            date_of_buy = form.cleaned_data['update_date']
            status = 2
            empik = form.cleaned_data['empik']
            tania = form.cleaned_data['tania_ksiazka']
            swiat = form.cleaned_data['swiat_ksiazki']
            user = User.objects.get(username=request.user.username)
            book = BooksToBuy.objects.create(user=user,
                                         title=title,
                                         author=author,
                                         publisher=publisher,
                                         update_date=date_of_buy,
                                         book_status=status,
                                         empik_price=empik,
                                         tania_ksiazka_price=tania,
                                         swiat_ksiazki_price=swiat)
            message = 'Gratulacje! książka została dodana! Możesz dodać następną.'
            ctx = {
                'message': message,
                'form': form,
            }
            return render(request, 'add_book_to_buy_form.html', context=ctx)

class DeleteBookBuy(View):
    """View used to delete book form database.
        Book was created via BooksToBuy model so this type of object is deleted."""
    def get(self, request, id):
        """Function to handle delete-book-to-buy's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        book = BooksToBuy.objects.get(id=id)
        books = BooksToBuy.objects.filter(title=book.title, author = book.title)
        name = book.title
        books.delete()
        message = f'Ksiażka: {name} została usunięta z bazy danych.'
        context = {
            "message": message
        }
        return render(request, 'delete_book_buy.html', context=context)

class MoveToBuyShopView(View):
    """View dedicated to move book to 'purchased' status.
     BooksToBuy model object is updated with data reated to purchase details: book_shop, book_price.
     MyBook model object is created as book is already in user's possession."""
    def get(self, request, id):
        """Function to handle add-bought-book-to-database's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        today = now().date()
        book = BooksToBuy.objects.get(id=id)
        books = BooksToBuy.objects.filter(title=book.title, author=book.author, update_date__lte=today).order_by('update_date').reverse()[0]
        form = ChooseShopForm()
        shops = {
            'Empik': books.empik_price,
            'Tania ksiażka': books.tania_ksiazka_price,
            'Świat książki': books.swiat_ksiazki_price
        }
        shopss = [(key, shops[key]) for key in shops]
        context = {
            "book": book,
            "form": form,
            "shops": shopss
        }
        return render(request, 'move_to_buy.html', context=context)
    def post(self, request, id):
        """Function to handle add-bought-book-to-database's request with post method

        Parameters:
        id (int): id number (from database) of chosen book"""
        form = ChooseShopForm(request.POST)
        if form.is_valid():
            shop = form.cleaned_data['shop']
            price = form.cleaned_data['price']
            book = BooksToBuy.objects.get(id=id)
            shops = {
                'Empik': book.empik_price,
                'Tania ksiażka': book.tania_ksiazka_price,
                'Świat książki': book.swiat_ksiazki_price
            }
            shopss = [(key, shops[key]) for key in shops]
            bookss = BooksToBuy.objects.filter(title=book.title, author=book.author)
            if  len(bookss) == 1:
                book.book_price = price
                book.book_shop = shop
                book.book_status = 1
                book.save()
            else:
                for elem in bookss:
                    elem.book_price = price
                    elem.book_shop = shop
                    elem.book_status = 1
                    elem.save()
            user = User.objects.get(username=request.user.username)
            book = MyBook.objects.create(user=user,
                                         title=book.title,
                                         author=book.author,
                                         publisher=book.publisher,
                                         date_of_buy=datetime.now(),
                                         status=1,
                                         rating=0)
            message = "Książka została dodana do biblioteki, gratuluję zakupu!"
            context = {
                "message": message,
                "form": form,
                "book": book,
                "shops": shopss
            }
            return render(request, 'move_to_buy.html', context=context)

class DeleteBookMyBook(View):
    """View dedicated to delete book from database."""
    def get(self, request, id):
        """Function to handle delete-book's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        book = MyBook.objects.get(id=id)
        name = book.title
        book.delete()
        message = f'Ksiażka: {name} została usunięta z bazy danych.'
        context = {
            "message": message
        }
        return render(request, 'delete_Mybook_buy.html', context=context)

class ProlongBookView(View):
    """View dedicated to prolong book borrowed from one of libraries"""
    def get(self, request, id):
        """Function to handle prolong-book's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        book = LibraryBooks.objects.get(id=id)
        form = PostponeReturnForm()
        context = {
            "book": book,
            "form": form,
        }
        return render(request, 'book_postpone.html', context=context)
    def post(self, request, id):
        """Function to handle prolong-book's request with post method

        Parameters:
        id (int): id number (from database) of chosen book"""
        form = PostponeReturnForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['return_date']
            book = LibraryBooks.objects.get(id=id)
            book.plan_return_date = date
            book.save()
            message = "Książka została przedłużona!"
            context = {
                "book": book,
                "form": form,
                "message": message
            }
            return render(request, 'book_postpone.html', context=context)

class ReturnBookView(View):
    """View dedicated to return book borrowed from one of libraries"""
    def get(self, request, id):
        """Function to handle return-library-book's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        book = LibraryBooks.objects.get(id=id)
        book.returned = True
        book.save()
        library = Library.objects.all().order_by('lib_name').distinct('lib_name')
        books = Library.objects.all().order_by('lib_name')
        paginator = Paginator(library, 5)
        page = request.GET.get('page')
        library = paginator.get_page(page)
        ctx = {
            "libraries" : library,
            "books" : books,
        }
        return render(request, 'lib_list.html', context=ctx)

class PlanListView(View):
    """View used to display list of created reading plans.
        Plans presented here are created via ReadingPlanA model presented in models.py dedicated file."""
    def get(self, request):
        """Function to handle display-plan-list's request with get method"""
        plan = ReadingPlanA.objects.all().order_by('plan_name').distinct('plan_name')
        paginator = Paginator(plan, 5)
        page = request.GET.get('page')
        plan = paginator.get_page(page)
        ctx = {
            'books': plan,
            'i': 0,
        }
        return render(request, 'plan_list.html', context=ctx)

class BookDetailView(View):
    """View dedicated to display details of chosen book"""
    def get(self, request, id):
        """Function to handle display-book-details's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        book = MyBook.objects.get(id=id)
        is_in_plan = PlanBooks.objects.filter(book=book)
        is_from_library = LibraryBooks.objects.filter(book=book)
        library = None
        if not is_from_library:
            pass
        else:
            library = Library.objects.filter(books=is_from_library[0])
        is_bought = BooksToBuy.objects.filter(title=book.title, author=book.author, book_status=1)
        if not is_bought:
            is_bought = None
        else:
            is_bought = is_bought[0]
        status = None
        if book.status == 1:
            status = "Nieprzeczytana"
        elif book.status == 2:
            status = "W trakcie czytania"
        else:
            status = "Przeczytana"

        ctx = {
            "book": book,
            "in_plan": is_in_plan,
            "from_library": is_from_library,
            "from_shop": is_bought,
            "library": library,
            "status": status
        }
        return render(request, 'book_details.html', context=ctx)

class DeleteFromPlanView(View):
    """View dedicated to delete book from chosen plan"""
    def get(self, request, id_plan, id_book):
        """Function to handle display-book-details's request with get method

        Parameters:
        id_plan (int): id number (from database) of chosen reading plan
        id_book (int): id number (from database) of chosen book"""
        plan = ReadingPlanA.objects.get(id=id_plan)
        book = MyBook.objects.get(id=id_book)
        planbook = PlanBooks.objects.filter(reading_plan=plan, book=book).delete()
        id = id_plan
        plans_count = ReadingPlanA.objects.count()
        if id in [i for i in range(1, plans_count + 1)]:
            plans = ReadingPlanA.objects.all()
            plan = plans[id - 1]
            read_books = PlanBooks.objects.filter(reading_plan=plan, is_read=True)
            books = []
            for i in range(len(read_books)):
                books.append(read_books[i].book)
            rest_books = PlanBooks.objects.filter(reading_plan=plan, is_read=False)
            bookss = []
            for i in range(len(rest_books)):
                bookss.append(rest_books[i].book)
            if PlanBooks.objects.filter(reading_plan=plan).count() != 0:
                num = int(read_books.count() / PlanBooks.objects.filter(reading_plan=plan).count() * 100)
            else:
                num = 0
            context = {
                'plan': plan,
                'read_book': books,
                'rest_book': bookss,
                'all_books': num,
                'percent': num

            }
            return render(request, "plan_details.html", context=context)

class MoveToReadStatePlanView(View):
    """View dedicated to move book state from 'Nieprzeczytana'/'W trakcie czytania' to 'Przeczytana'"""
    def get(self, request, id_plan, id_book):
        """Function to handle mark-book-as-read's request with get method

        Parameters:
        id_plan (int): id number (from database) of chosen reading plan
        id_book (int): id number (from database) of chosen book"""
        plan = ReadingPlanA.objects.get(id=id_plan)
        book = MyBook.objects.get(id=id_book)
        planbook = PlanBooks.objects.filter(reading_plan=plan, book=book)[0]
        planbook.is_read = True
        planbook.save()
        book.status = 3
        book.save()
        id = id_plan
        plans_count = ReadingPlanA.objects.count()
        if id in [i for i in range(1, plans_count + 1)]:
            plans = ReadingPlanA.objects.all()
            plan = plans[id - 1]
            read_books = PlanBooks.objects.filter(reading_plan=plan, is_read=True)
            books = []
            for i in range(len(read_books)):
                books.append(read_books[i].book)
            rest_books = PlanBooks.objects.filter(reading_plan=plan, is_read=False)
            bookss = []
            for i in range(len(rest_books)):
                bookss.append(rest_books[i].book)
            if PlanBooks.objects.filter(reading_plan=plan).count() != 0:
                num = int(read_books.count() / PlanBooks.objects.filter(reading_plan=plan).count() * 100)
            else:
                num = 0
            context = {
                'plan': plan,
                'read_book': books,
                'rest_book': bookss,
                'all_books': num,
                'percent': num

            }
            return render(request, "plan_details.html", context=context)

class DeleteBookMyBookMainDBView(View):
    """View dedicated to delete book from database."""
    def get(self, request, id):
        """Function to handle delete-book's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        book = MyBook.objects.get(id=id)
        name = book.title
        book.delete()
        message = f'Ksiażka: {name} została usunięta z bazy danych.'
        context = {
            "message": message
        }
        return render(request, 'delete_Mybook.html', context=context)
    
class EditBookView(View):
    def get(self, request, id):
        message=None
        book = MyBook.objects.get(id=id)
        status = None
        if book.status == 1:
            status = "Nieprzeczytana"
        elif book.status == 2:
            status = "W trakcie czytania"
        else:
            status = "Przeczytana"
        context = {
            'book': book,
            'message' : message,
            'status' : status
        }
        return render(request, "edit_book_detail.html", context=context)
    def post(self, request, id):
        publisher = request.POST.get("publisher")
        status = request.POST.get("status")
        if status == "Nieprzeczytana":
            status = 1
        elif book.status == "W trakcie czytania":
            status = 2
        else:
            status = 3
        date_of_buy = request.POST.get("date_of_buy")
        rating = request.POST.get("rating")
        review = request.POST.get("resume")
        if publisher and status and date_of_buy and rating and review:
            book = MyBook.objects.get(id=id)
            book.publisher = publisher
            book.date_of_buy = date_of_buy
            book.status = status
            book.rating = rating
            book.review = review
            book.save()
            return redirect('book-detail', id=book.id)
        else:
            book = MyBook.objects.get(id=id)
            massage = "Wypełnij dokładnie wszystkie pola!"
            status = None
            if book.status == 1:
                status = "Nieprzeczytana"
            elif book.status == 2:
                status = "W trakcie czytania"
            else:
                status = "Przeczytana"
            context = {
                'book': book,
                'message' : massage,
                'status' : status
            }
            return render(request, "edit_book_detail.html", context=context)
        
class AddPricesView(View):
    def get(self, request, id):
        """Function to handle prolong-book's request with get method

        Parameters:
        id (int): id number (from database) of chosen book"""
        today = now().date()
        book = BooksToBuy.objects.get(id=id)
        books = BooksToBuy.objects.filter(title=book.title, author=book.author, update_date__lte=today).order_by('update_date').reverse()[0]
        form = AddPricesForm()
        context = {
            "book": books,
            "form": form,
        }
        return render(request, 'book_add_price.html', context=context)
    def post(self, request, id):
        """Function to handle prolong-book's request with post method

        Parameters:
        id (int): id number (from database) of chosen book"""
        form = AddPricesForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['update_date']
            empik = form.cleaned_data['empik']
            tania_ksiazka = form.cleaned_data['tania_ksiazka']
            swiat_ksiazki = form.cleaned_data['swiat_ksiazki']
            book = BooksToBuy.objects.get(id=id)
            book.pk = None
            book.update_date = date
            book.empik_price = empik
            book.tania_ksiazka_price = tania_ksiazka
            book.swiat_ksiazki_price = swiat_ksiazki
            book.save()
            return redirect('detail-price', id=book.id)
        
class PriceDetailView(View):
    def get(self, request, id):
        book = BooksToBuy.objects.get(id=id)
        books = BooksToBuy.objects.filter(title = book.title, author = book.author)
        context = {
            "book": book,
            "books": books,
        }
        return render(request, 'price_detail.html', context=context)
