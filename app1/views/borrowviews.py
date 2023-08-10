from django.shortcuts import render, redirect, get_object_or_404
from app1 import models
from datetime import date


def borrowing_list(request):
    """
    借阅列表
    :param request:
    :return:
    """
    if request.session["user"] == "admin":
        current_borrower_username = request.session.get('info')
        try:
            borrower = models.Admin.objects.get(username=current_borrower_username)
        except models.Borrower.DoesNotExist:
            borrower = None
        borrowings = models.AdminBorrowing.objects.filter(borrower=borrower)
        return render(request, 'AdminTemplates/AdBorrowTemplates/admin_borrow_list.html', {'borrowings': borrowings})

    current_borrower_username = request.session.get('info')
    try:
        borrower = models.Borrower.objects.get(username=current_borrower_username)
    except models.Borrower.DoesNotExist:
        borrower = None
    borrowings = models.ComBorrowing.objects.filter(borrower=borrower)
    return render(request, 'CommonTemplates/BorrowTemplates/com_borrow_list.html', {'borrowings': borrowings})


def borrow_book(request, book_id):
    """
    借阅图书
    :param request:
    :param book_id: 图书id
    :return:
    """
    book = get_object_or_404(models.Book, pk=book_id)

    if request.method == 'POST':
        borrower_username = request.POST.get('borrower_username')
        borrowed_date = date.today()

        if request.session.get('info') != borrower_username:
            error_message = "输入的用户名与当前借阅人不匹配。"
            if request.session["user"] == "admin":
                return render(request, "AdminTemplates/AdBorrowTemplates/admin_borrow_book.html", {'book': book, 'error_message': error_message})
            return render(request, 'CommonTemplates/BorrowTemplates/com_borrow_book.html', {'book': book, 'error_message': error_message})

        book.account += 1
        book.save()

        if request.session["user"] == "admin":

            borrower, created = models.Admin.objects.get_or_create(username=borrower_username)
            borrowing = models.AdminBorrowing.objects.create(book=book, borrower=borrower, borrowed_date=borrowed_date)
            borrowing.save()

        else:
            borrower, created = models.Borrower.objects.get_or_create(username=borrower_username)
            borrowing = models.ComBorrowing.objects.create(book=book, borrower=borrower, borrowed_date=borrowed_date,)
            borrowing.save()
        return redirect('book_list')

    if request.session["user"] == "admin":
        return render(request, "AdminTemplates/AdBorrowTemplates/admin_borrow_book.html", {'book': book})
    return render(request, 'CommonTemplates/BorrowTemplates/com_borrow_book.html', {'book': book})


def return_book(request, borrowing_id):
    """
    归还图书
    :param request:
    :param borrowing_id: 图书id
    :return:
    """
    if request.session["user"] == "admin":
        borrowing = get_object_or_404(models.AdminBorrowing, pk=borrowing_id)
    else:
        borrowing = get_object_or_404(models.ComBorrowing, pk=borrowing_id)

    current_borrower = request.session.get('info')
    if current_borrower and borrowing.borrower.username == current_borrower:
        if request.method == 'POST':
            borrowing.returned_date = date.today()
            borrowing.save()
            book = borrowing.book
            book.available = True
            book.save()
            return redirect('borrowing_list')
    else:
        return redirect('book_list')

    if request.session["user"] == "admin":
        return render(request, 'AdminTemplates/AdBorrowTemplates/admin_return_book.html', {'borrowing': borrowing})
    return render(request, 'CommonTemplates/BorrowTemplates/com_return_book.html', {'borrowing': borrowing})
