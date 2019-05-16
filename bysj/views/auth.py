import hashlib
import pymysql
from django.shortcuts import render, redirect, reverse, HttpResponse
from bysj import models
from bysj.forms import RegForm, UserInfoForm
from django.utils.safestring import mark_safe
from django.conf import settings



def index(request):
    conn = pymysql.connect(
        host='127.0.0.source',
        port=3306,
        user='root',
        password='',
        database='mooc_course',
        charset='utf8'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from computer;"
    cursor.execute(sql)  # res我们说是得到的行数，如果这个行数不为零，说明用户输入的用户名和密码存在，如果为0说名存在，你想想对不
    obj = mark_safe(cursor.fetchall())
    print(obj)
    conn.close()
    return render(request,'index.html',{"obj":obj})
# 登陆
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()

        obj = models.UserInfo.objects.filter(username=user, password=pwd, is_active=True).first()
        if obj:
            # 登录成功 跳转到主页面
            # 保存当前用户的id
            request.session['pk'] = obj.pk
            # print(obj.pk)
            a = models.UserInfo.objects.filter(id=obj.pk).values('roles').first() # {'roles': 2}
            request.session['qx'] = a['roles']

            # 保存用户的权限
            permission_query = obj.roles.filter().values('permission__url',
                                                        'permission__title',
                                                        'permission__icon',
                                                        'permission__is_menu',
                                                        ).distinct()
            # print(permission_query)
            # 权限列表
            permission_list = []
            #  菜单列表
            menu_list = []

            for i in  permission_query:
                permission_list.append({'url':i['permission__url']})
                if i['permission__is_menu']:
                    menu_list.append({'url':i['permission__url'],
                                      'title':i['permission__title'],
                                      'icon':i['permission__icon'],
                                      })

            request.session[settings.PERMISSION_SESSION_KEY] = list(permission_list) # json序列化
            request.session[settings.MENU_SESSION_KEY] = menu_list
            # print(menu_list)
            return redirect(reverse('index'))
        else:
            # 登录失败
            # return HttpResponse('账号或密码错误')
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')


# 注册
def reg(request):
    # 判断请求方式
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        # print(request.POST)
        # print("?????????????????", form_obj)
        # 对数据进行校验
        if form_obj.is_valid():
            print('111')
            # 数据正确 插入数据库
            print(form_obj.cleaned_data)
            # form_obj.cleaned_data.pop('re_password')
            # models.UserProfile.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(reverse('login'))
        else:
            print(form_obj.errors)

    else:
        form_obj = RegForm()

    return render(request, 'reg.html', {'form_obj': form_obj})


# 注销
def logout(request):
    del request.session['pk']
    return redirect(reverse('login'))

# 个人信息修改
def ge(request):
    ids = request.session['pk']
    # print(ids)

    obj = models.UserInfo.objects.filter(pk=ids).first()
    # print('----',obj)
    if request.method == "POST":
        form_obj = UserInfoForm(request.POST, instance=obj)
        print(request.POST.get('name'))
        if form_obj.is_valid():
            print('111')
            form_obj.save()  # 保存修改
            # 跳转到展示页面
            return redirect(reverse('ge'))
    else:
        form_obj = UserInfoForm(instance=obj)
    return render(request, 'ge.html', {"form_obj":form_obj})




# 用户管理
def userinfo_change(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        for i in ids:
            models.UserInfo.objects.filter(id=int(i)).delete()
    obj = models.UserInfo.objects.all()
    return render(request, 'userinfo.html',{'obj':obj})

# def userinfo_edit(request, uid):
