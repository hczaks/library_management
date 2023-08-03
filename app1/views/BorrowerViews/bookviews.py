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
    if request.session["user"] == "admin":
        return render(request, 'AdminTemplates/AdBookTemplates/admin_list_book.html', {'books': books})
    return render(request, 'CommonTemplates/BookTemplates/com_list_book.html', {'books': books})


def admin_add_book(request):
    """
    添加图书
    :param request:
    :return:
    """
    if request.session["user"] != "admin":
        return render(request, 'CommonTemplates/BookTemplates/com_list_book.html')

    if request.method == 'GET':
        form = BookForm()
        return render(request, 'AdminTemplates/AdBookTemplates/admin_add_book.html', {'form': form})

    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.published_date = form.cleaned_data['ctime']
        book.save()
        return redirect('book_list')
    return render(request, 'AdminTemplates/AdBookTemplates/admin_add_book.html', {'form': form})


def admin_edit_book(request, book_id):
    """
    编辑图书
    :param request:
    :param book_id: 图书id
    :return:
    """
    if request.session["user"] != "admin":
        return render(request, 'CommonTemplates/BookTemplates/com_list_book.html')

    book = get_object_or_404(models.Book, pk=book_id)
    if request.method == 'GET':
        form = BookForm(instance=book, initial={'ctime': book.published_date})

    elif request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.published_date = form.cleaned_data['ctime']
            form.save()
            return redirect('book_list')
    return render(request, 'AdminTemplates/AdBookTemplates/admin_edit_book.html', {'form': form, 'book': book})


def admin_delete_book(request, book_id):
    """
    删除图书
    :param request:
    :param book_id: 图书id
    :return:
    """
    if request.session["user"] != "admin":
        return render(request, 'CommonTemplates/BookTemplates/com_list_book.html')

    book = get_object_or_404(models.Book, pk=book_id)
    book.delete()
    return redirect('book_list')





