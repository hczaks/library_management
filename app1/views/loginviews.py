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







