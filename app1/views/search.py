from django.shortcuts import render

from app1.models import Book


def search(request):
    """
    查询功能
    :param request:
    :return:
    """
    books = None
    if request.method == 'POST':
        query = request.POST.get('search')
        books = Book.objects.filter(title__icontains=query) | \
                Book.objects.filter(number__icontains=query) | \
                Book.objects.filter(author__icontains=query)

    if request.session["user"] == "admin":
        return render(request, 'AdminTemplates/AdBookTemplates/admin_search_book.html', {'books': books})

    return render(request, 'CommonTemplates/BookTemplates/com_search_book.html', {'books': books})
