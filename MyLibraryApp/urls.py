"""
URL configuration for MyLibraryApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from biblioteka.views import (
    # StartSideView,
    AddBookView,
    BookListView,
    LoginUser,
    LogoutUser,
    AddUser,
    LandingPageView,
    ShoppingListView,
    LibraryListView,
    RankingView,
    StatisticsView,
    AddLibBookView,
    ReadingPlanAddView,
    AddBookToPlanView,
    ReadingPlanDetailView,
    AddBookToBuyView,
    DeleteBookBuy,
    MoveToBuyShopView,
    DeleteBookMyBook,
    ProlongBookView,
    ReturnBookView,
    PlanListView,
    BookDetailView,
    DeleteFromPlanView,
    MoveToReadStatePlanView,
    DeleteBookMyBookMainDBView

)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', StartSideView.as_view(), name='start-side'),
    path('add_book/', AddBookView.as_view(), name='add-book'),
    path('book_list/', BookListView.as_view(), name='book-list'),
    path('login_user/', LoginUser.as_view(), name='login-user'),
    path('logout_user/', LogoutUser.as_view(), name='logout-user'),
    path('add_user/', AddUser.as_view(), name='add-user'),
    path('', LandingPageView.as_view(), name='index-view'),
    path('shopping_list/', ShoppingListView.as_view(), name='shopping-list'),
    path('library_list/', LibraryListView.as_view(), name='library-list'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('add_lib/', AddLibBookView.as_view(), name='add-lib-book'),
    path('plan/add', ReadingPlanAddView.as_view(), name='add-plan'),
    path('plan/add_book', AddBookToPlanView.as_view(), name='add-book-plan'),
    path('plan/<int:id>', ReadingPlanDetailView.as_view(), name='plan-detail'),
    path('add_book_buy', AddBookToBuyView.as_view(), name='add-book-buy'),
    path('delete_book_buy/<int:id>', DeleteBookBuy.as_view(), name='delete-buy'),
    path('move_to_bought/<int:id>', MoveToBuyShopView.as_view(), name='book-bought'),
    path('delete_book/<int:id>', DeleteBookMyBook.as_view(), name='delete-book'),
    path('prolong/<int:id>', ProlongBookView.as_view(), name='prolong-book'),
    path('return_book/<int:id>', ReturnBookView.as_view(), name='return-book'),
    path('plan_list/', PlanListView.as_view(), name='plan-list'),
    path('book_detail/<int:id>', BookDetailView.as_view(), name='book-detail'),
    path('plan/<int:id_plan>/<int:id_book>', DeleteFromPlanView.as_view(), name='delete-from-plan'),
    path('plan_delete/<int:id_plan>/<int:id_book>', MoveToReadStatePlanView.as_view(), name='move-to-read'),
    path('book_delete/<int:id>', DeleteBookMyBookMainDBView.as_view(), name='delete-book-mybook')
]
