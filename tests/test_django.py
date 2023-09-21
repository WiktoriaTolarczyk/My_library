import pytest
from biblioteka.models import MyBook, BooksToBuy, Library, LibraryBooks, MONTHS, get_author_rate, ReadingPlanA, PlanBooks
from biblioteka.forms import AddBookForm
from django.test import Client
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.core.paginator import Paginator

@pytest.mark.django_db
def test_add_book_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = Client()
    client.login(username='testuser', password='testpassword')
    response_get = client.get(reverse('add-book'))
    assert response_get.status_code == 200

    form_data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'publisher': 'Test Publisher',
        'date_of_buy': '2023-09-21',
        'status': 1,
        'rating': 5,
        'review': 'Test review',
    }
    response_post = client.post(reverse('add-book'), data=form_data)
    assert response_post.status_code == 200
    assert MyBook.objects.filter(title='Test Book').exists()

    user.delete()

@pytest.mark.django_db
def test_login_user_view():
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)
    client = Client()
    response_get = client.get(reverse('login-user'))
    assert response_get.status_code == 200

    form_data = {
        'username': username,
        'password': password,
    }
    response_post = client.post(reverse('login-user'), data=form_data)
    assert response_post.status_code == 200
    assert response_post.context['user'].is_authenticated

    user.delete()

@pytest.mark.django_db
def test_book_list_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = Client()
    client.login(username='testuser', password='testpassword')

    for i in range(20):
        MyBook.objects.create(user=user,
                            title=f'Test Book',
                            author=f'Test Author {i}',
                            publisher=f'Test Publisher {i}',
                            date_of_buy='2023-09-21',
                            status=1,
                            rating=5,
                            review=f'Test review {i}')

    response = client.get(reverse('book-list'))
    assert response.status_code == 200
    assert len(response.context['books']) == 10

    user.delete()
    MyBook.objects.filter(title='Test Book').delete()


@pytest.mark.django_db
def test_landing_page_view():
    client = Client()
    response = client.get(reverse('index-view'))
    assert response.status_code == 200

