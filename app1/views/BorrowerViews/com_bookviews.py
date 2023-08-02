from django.shortcuts import render, redirect, get_object_or_404
from app1.form import BookForm
from app1 import models


def book_list(request):
    """
    图书列表
    :param request:
    :return:
    """
    # 图书列表
    books = models.Book.objects.all()
    return render(request, 'CommonTemplates/BookTemplates/com_list_book.html', {'books': books})




