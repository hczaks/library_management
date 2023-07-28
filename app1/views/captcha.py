from io import BytesIO
from django.http import HttpResponse
from app1 import code


def image_code(request):
    """
    生产验证码
    :param request:
    :return:
    """
    # 调用pillow函数，生成图片
    img, code_string = code.check_code()

    # 写入到session中
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())