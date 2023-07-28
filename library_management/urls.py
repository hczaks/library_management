"""library_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from app1.views import loginviews, borrowingviews, bookviews, captcha


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginviews.login, name='login'),
    path('logout', loginviews.logout, name='logout'),
    path('register/', loginviews.register, name='register'),


    path('books/', bookviews.book_list, name='book_list'),
    path('books/add/', bookviews.add_book, name='add_book'),
    path('books/delete/<int:book_id>/', bookviews.delete_book, name='delete_book'),
    path('books/edit/<int:book_id>/', bookviews.edit_book, name='edit_book'),


    path('books/borrow/<int:book_id>', borrowingviews.borrow_book, name='borrow_book'),
    path('books/return/<int:borrowing_id>', borrowingviews.return_book, name='return_book'),
    path('borrowings/', borrowingviews.borrowing_list, name='borrowing_list'),


    path('image/code/', captcha.image_code, name='image_code')
]
