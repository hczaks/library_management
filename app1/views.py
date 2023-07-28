from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from app1.form import LoginForm, BorrowerForm, BookForm
from app1 import models, code
from datetime import date
from io import BytesIO

RootUser = "1234567"


def login(request):
    """
    登录视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user_input_code = form.cleaned_data.pop('code')
            code = request.session.get('image_code', "")
            if user_input_code.upper() != code.upper():
                form.add_error("code", "验证码错误")
                return render(request, 'login.html', {'form': form})

            for obj in models.Borrower.objects.all():
                if {username, password} == {obj.username, obj.password}:
                    request.session["info"] = username
                    # session可以保存7天
                    request.session.set_expiry(60 * 60 * 24 * 7)
                    return redirect('book_list')
            form.add_error("password", "用户名或者密码错误")

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    """
    注销视图
    :param request:
    :return:
    """
    # 注销
    request.session.clear()
    return redirect('login')


def register(request):
    """
    注销
    :param request:
    :return:
    """
    # 注册用户
    if request.method == 'GET':
        form = BorrowerForm()
        return render(request, 'register.html', {'form': form})
    form = BorrowerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def book_list(request):
    """
    图书列表
    :param request:
    :return:
    """
    # 图书列表
    books = models.Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def add_book(request):
    # 添加图书
    if request.session.get("info") != RootUser:
        return HttpResponse("无权访问")

    if request.method == 'GET':
        form = BookForm()
        return render(request, 'add_book.html', {'form': form})

    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.published_date = form.cleaned_data['ctime']
        book.save()
        return redirect('book_list')
    return render(request, 'add_book.html', {'form': form})


def edit_book(request, book_id):
    # 编辑图书
    if request.session.get("info") != RootUser:
        return HttpResponse("无权访问")

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
    return render(request, 'edit_book.html', {'form': form, 'book': book})


def delete_book(request, book_id):
    # 删除图书
    if request.session.get("info") != RootUser:
        return HttpResponse("无权访问")

    book = get_object_or_404(models.Book, pk=book_id)
    book.delete()
    return redirect('book_list')


def borrowing_list(request):
    # 借阅列表
    current_borrower_username = request.session.get('info')
    borrower = models.Borrower.objects.get(username=current_borrower_username)
    borrowings = models.Borrowing.objects.filter(borrower=borrower)
    return render(request, 'borrowing_list.html', {'borrowings': borrowings})


def borrow_book(request, book_id):
    # 借阅图书
    book = get_object_or_404(models.Book, pk=book_id)

    if request.method == 'POST':
        borrower_username = request.POST.get('borrower_username')
        borrowed_date = date.today()

        borrower, created = models.Borrower.objects.get_or_create(username=borrower_username)
        if request.session.get('info') != borrower_username:
            error_message = "输入的用户名与当前借阅人不匹配。"
            return render(request, 'borrow_book.html', {'book': book, 'error_message': error_message})

        borrowing = models.Borrowing.objects.create(book=book, borrower=borrower, borrowed_date=borrowed_date)
        borrowing.save()
        return redirect('book_list')

    return render(request, 'borrow_book.html', {'book': book})


def return_book(request, borrowing_id):
    # 归还图书
    borrowing = get_object_or_404(models.Borrowing, pk=borrowing_id)
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

    return render(request, 'return_book.html', {'borrowing': borrowing})


def image_code(request):
    # 调用pillow函数，生成图片
    img, code_string = code.check_code()

    # 写入到session中
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


