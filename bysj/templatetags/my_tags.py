import re
from django import template
from django.urls import reverse
from django.http.request import QueryDict
from django.conf import settings
register = template.Library()



@register.simple_tag
def reverse_url(request, url_name, *args, **kwargs):
    # 获取当前地址  下次操作完成后跳转回来
    # /bysj/book_list/?page=source&query=python
    next = request.get_full_path()

    # 生成一个QueryDict对象  可编辑
    qd = QueryDict(mutable=True)
    qd['next'] = next  #
    # URL反向解析
    base_url = reverse(url_name, args=args, kwargs=kwargs)

    return '{}?{}'.format(base_url, qd.urlencode())

@register.inclusion_tag('menu.html')
def menu(request, ):
    # 当前访问地址
    url = request.path_info

    menu_list = request.session[settings.MENU_SESSION_KEY]
    # print(menu_list)
    for i in menu_list:
        if re.match("^{}$".format(i['url']), url):
            i['class'] = 'active'
    return {'menu_list':menu_list}