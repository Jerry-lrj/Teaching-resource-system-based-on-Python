import pymysql
import os
from django.shortcuts import render, reverse, redirect, HttpResponse
from utils.pagination import Pagination
from bysj import models

# 更新推荐数量
def update(tj):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='mooc_course',
        charset='utf8'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # sql = "select * from computer name like '%{}%' order by order_num;".format(q)
    sql = "update computer set commend = commend + 1 where order_num=%d;" % int(tj)
    # print(sql)
    cursor.execute(sql)
    cursor.fetchall()
    # all = cursor.execute(sql)
    # obj = cursor.fetchall()
    # print(obj)
    # print(all)
    conn.commit()
    conn.close()

# 讲选中的书籍存到booklist表中
def post_book(request):

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='mooc_course',
        charset='utf8'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    for el in request.POST.getlist('ids'):
        sql = "select * from computer where order_num=%d;" % int(el)
        cursor.execute(sql)
        courses = cursor.fetchall()
        # print('我是 ', courses)

        for i in courses:
            # print('》》》》》',i)
            pk = request.session.get('pk')
            print(models.BookList.objects.filter(order_num=i['order_num'], userinfos_id=pk).first())
            if  models.BookList.objects.filter(order_num=i['order_num'], userinfos_id=pk).first():
                print('插入失败')
                raise Exception('添加失败')   #####  改这个
                # conn.close()
                # return render(request, 'login.html')
            else:
                models.BookList.objects.create(order_num=i['order_num'], course=i['course'], school=i['school'],
                                               teacher=i['teacher'], stu_num=i['stu_num'],
                                               introduction=i['introduction'], link=i['link'], userinfos_id=pk)
                print('数据添加成功')
    conn.close()

    return render(request, 'book_list.html')

# 推荐排行
def index(request):
    """
    展示推荐最高的前10个数据        user='root',

    :param request:
    :return:
    """
    if request.method == 'POST':
        print(request.POST.get())
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='mooc_course',
        charset='utf8'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from computer order by commend desc  limit 10 ;"
    cursor.execute(sql)  # res我们说是得到的行数，如果这个行数不为零，说明用户输入的用户名和密码存在，如果为0说名存在，你想想对不
    obj = cursor.fetchall()
    # print(obj)
    conn.close()
    return render(request, 'index.html', {"obj": obj})

# 展示课程
def book_list(request):
    q = request.GET.get('query', '')  # 取搜索条件
    # print(q)
    # for i in  request.POST.getlist('ids'): # 取书籍的order_num, 字符串
    #     print(i, type(i))
    if request.method == 'POST':
        # print('---------', request.POST.get('ids'))
        post_book(request) # 提交书籍函数
    tj = request.GET.get('tid', '')
    print(tj)
    if tj :
        # print(tj)
        update(tj) # 调用update函数
        return redirect(reverse('book_list'))
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='mooc_course',
        charset='utf8'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # sql = "select * from computer name like '%{}%' order by order_num;".format(q)
    if q:
        sql = "select * from computer where course like '%{}%' order by order_num;".format(q)
    else:  # 当q为空, 显示所有书籍信息
        sql = "select * from computer order by order_num;"
    all = cursor.execute(sql)  # 得到的行数
    obj = cursor.fetchall()
    # print(obj)
    conn.close()
    page = Pagination(request.GET.get('page', 1), all, request.GET.copy())
    return render(request, 'book_list.html', {"obj": obj[page.start:page.end], 'page_html': page.page_html})




# 展示用户收藏的课程
def my_book_list(request):
    # return HttpResponse('op')
    pk = request.session.get('pk')
    # print(pk) # 用户id
    obj = models.BookList.objects.filter(userinfos_id=pk)
    # print(obj) # <QuerySet [<BookList: Python语言程序设计>, <BookList: Office高级应用>, <BookList: 数据结构>]>
    all = obj.count()
    # return HttpResponse('ok')
    # return  render(request, 'my_book_list.html', {"obj":obj})
    ids = request.POST.getlist('ids') # 需要移除书籍的order_num号
    print(ids)
    if request.method == "POST":
        for el in ids:
            print(el, type(el))
            models.BookList.objects.filter(order_num=el, userinfos_id=pk).delete()
    page = Pagination(request.GET.get('page', 1), all)
    return render(request, 'my_book_list.html', {"obj": obj[page.start:page.end], 'page_html': page.page_html})

# 推荐课程, 更新推荐数
def book_tj(request, ids):
    print(ids)
    return render(request, 'book_list.html')


# 更新所有课程
def book_update(request):
    os.system("python mooc.py")
    return HttpResponse('更新')

# 公告
def annunciate(request):
    annunciate_obj = models.annunciate.objects.all()
    # print('========', request.session['qx'])
    qx = request.session['qx']
    if qx != 1:
        qx = None
    print('>>>>>>>',qx)
    if request.method == 'POST':
        # print(request.POST.get('text'))
        msg = request.POST.get('text')
        models.annunciate.objects.create(msg=msg)
    return render(request, 'annunciate.html',{'annunciate_obj':annunciate_obj,'qx':qx})

# 留言
def comment(request):

    comment_obj = models.user_liuyan.objects.all().order_by('-date')
    if request.method == 'POST':
        # print('>>>>',request.session['pk'])
        user_id = request.session['pk']
        # print(request.POST.get('text'))
        msg = request.POST.get('text')
        models.user_liuyan.objects.create(
            user_id=user_id,
            message=msg,
        )
    return render(request, 'comment.html',{'comment_obj':comment_obj})




