# 登陆认证
import re
from django.utils.deprecation import MiddlewareMixin
from bysj import models
from django.shortcuts import redirect, reverse, HttpResponse
from django.conf import settings
class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 获取当前访问页面
        url = request.path_info
        # print(url)
        for i in settings.WHITE_LIST:
            if re.match(i, url):
                return
        pk = request.session.get('pk')
        # print(pk)
        user = models.UserInfo.objects.filter(pk=pk).first()
        # 没有登录 跳转至登录页面
        if not user:
            return redirect(reverse('login'))

        request.user_obj = user

        # 获取当前用户的权限
        permission_list = request.session[settings.PERMISSION_SESSION_KEY]
        # 打印当前用户拥有的权限
        # print(permission_list)
        for i in permission_list:

            if re.match('^{}$'.format(i['url']), url):
                return
        # 没有匹配成功
        return HttpResponse('没有权限')
