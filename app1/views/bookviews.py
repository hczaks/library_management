from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from app1.form import LoginForm, BorrowerForm, BookForm
from app1 import models, code


def book_list(request):
    """
    图书列表
    :param request:
    :return:
    """
    # 图书列表
    books = models.Book.objects.all()
    return render(request, 'BookTemplates/list_book.html', {'books': books})


def add_book(request):
    # 添加图书
    # if request.session.get("info") != RootUser:
    #     return HttpResponse("无权访问")

    if request.method == 'GET':
        form = BookForm()
        return render(request, 'BookTemplates/add_book.html', {'form': form})

    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.published_date = form.cleaned_data['ctime']
        book.save()
        return redirect('book_list')
    return render(request, 'BookTemplates/add_book.html', {'form': form})


def edit_book(request, book_id):
    # 编辑图书
    # if request.session.get("info") != RootUser:
    #     return HttpResponse("无权访问")

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
    return render(request, 'BookTemplates/edit_book.html', {'form': form, 'book': book})


def delete_book(request, book_id):
    # 删除图书
    # if request.session.get("info") != RootUser:
    #     return HttpResponse("无权访问")

    book = get_object_or_404(models.Book, pk=book_id)
    book.delete()
    return redirect('book_list')


