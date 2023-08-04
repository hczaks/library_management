from django.shortcuts import render

from app1.models import Admin, Borrower


def information(request):
    """
    个人信息
    :param request:
    :return:
    """
    if request.session["user"] == "admin":
        return render(request, 'AdminTemplates/admin_information.html')
    else:
        user = Borrower.objects.filter(username=request.session["info"])
        return render(request, 'CommonTemplates/com_information.html', {'user': user})
