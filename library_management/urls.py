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
from django.urls import path
from app1.views import captcha, loginviews, bookviews, borrowviews, search, information

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', loginviews.login, name='login'),
    path('logout/', loginviews.logout, name='logout'),
    path('register/', loginviews.register, name='register'),
    path('admin/login/', loginviews.login, name='admin_login'),

    # 验证码
    path('image/code/', captcha.image_code, name='image_code'),

    path('information/', information.information, name='information'),
    # 普通用户url
    path('books/', bookviews.book_list, name='book_list'),
    path('books/search/', search.search, name='search'),
    path('books/borrow/<int:book_id>', borrowviews.borrow_book, name='borrow_book'),
    path('books/return/<int:borrowing_id>', borrowviews.return_book, name='return_book'),
    path('borrow/', borrowviews.borrowing_list, name='borrowing_list'),
    path('books/add/', bookviews.admin_add_book, name='add_book'),
    path('books/delete/<int:book_id>/', bookviews.admin_delete_book, name='delete_book'),
    path('books/edit/<int:book_id>/', bookviews.admin_edit_book, name='edit_book'),
    #
    # # 管理员url
    # path('admin/books/', admin_bookviews.admin_book_list, name='admin_book_list'),
    #
    # path('admin/borrow/', admin_borrowviews.borrowing_list, name='admin_borrowing_list'),


]
