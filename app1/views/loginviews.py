from django.shortcuts import render, redirect
from app1.form import LoginForm, BorrowerForm
from app1 import models


def login(request):
    """
    登录视图
    :param request:
    :return:
    """
    global bl
    bl = False
    if request.method == 'POST':

        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user_input_code = form.cleaned_data.pop('code')
            code = request.session.get('image_code', "")
            if user_input_code.upper() != code.upper():
                form.add_error("code", "验证码错误")
                return render(request, 'LoginTemplates/login.html', {'form': form})

            current_url = request.build_absolute_uri()
            if current_url == "http://127.0.0.1:8000/admin/login/":
                bl = True
            print(bl)
            if bl:
                for obj in models.Admin.objects.all():
                    if {username, password} == {obj.username, obj.password}:
                        request.session["info"] = username
                        # session可以保存7天
                        request.session.set_expiry(60 * 60 * 24 * 7)
                        print("_______________")
                        return redirect('admin_book_list')
            else:
                for obj in models.Borrower.objects.all():
                    if {username, password} == {obj.username, obj.password}:
                        request.session["info"] = username
                        # session可以保存7天
                        request.session.set_expiry(60 * 60 * 24 * 7)
                        return redirect('book_list')
            form.add_error("password", "用户名或者密码错误")

    form = LoginForm()
    return render(request, 'LoginTemplates/login.html', {'form': form})


def logout(request):
    """
    注销视图
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('login')


def register(request):
    """
    注册账号
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = BorrowerForm()
        return render(request, 'LoginTemplates/register.html', {'form': form})
    form = BorrowerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'LoginTemplates/register.html', {'form': form})

