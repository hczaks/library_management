from django.shortcuts import render, redirect, get_object_or_404
from app1.form import BookForm
from app1 import models


def admin_book_list(request):
    """
    图书列表
    :param request:
    :return:
    """
    # 图书列表
    books = models.Book.objects.all()
    return render(request, 'AdminTemplates/AdBookTemplates/admin_list_book.html', {'books': books})


def admin_add_book(request):
    """
    添加图书
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = BookForm()
        return render(request, 'AdminTemplates/AdBookTemplates/admin_add_book.html', {'form': form})

    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.published_date = form.cleaned_data['ctime']
        book.save()
        return redirect('admin_book_list')
    return render(request, 'AdminTemplates/AdBookTemplates/admin_add_book.html', {'form': form})


def admin_edit_book(request, book_id):
    """
    编辑图书
    :param request:
    :param book_id: 图书id
    :return:
    """
    book = get_object_or_404(models.Book, pk=book_id)
    if request.method == 'GET':
        form = BookForm(instance=book, initial={'ctime': book.published_date})

    elif request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.published_date = form.cleaned_data['ctime']
            form.save()
            return redirect('admin_book_list')
    return render(request, 'AdminTemplates/AdBookTemplates/admin_edit_book.html', {'form': form, 'book': book})


def admin_delete_book(request, book_id):
    """
    删除图书
    :param request:
    :param book_id: 图书id
    :return:
    """
    book = get_object_or_404(models.Book, pk=book_id)
    book.delete()
    return redirect('admin_book_list')


