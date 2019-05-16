from django.db import models

# Create your models here.
# 权限
class Permission(models.Model):

    url = models.CharField('权限', max_length=32)
    title = models.CharField('标题', max_length=32)
    is_menu = models.BooleanField('是否是菜单',default=False)
    icon = models.CharField('图标', max_length=100, null=True, blank=True)
    def __str__(self):
        return self.title
# 角色
class Role(models.Model):

    name = models.CharField('角色名称', max_length=32)
    permission = models.ManyToManyField('Permission', verbose_name='角色拥有权限')

    def __str__(self):
        return self.name
# 用户
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.EmailField(verbose_name='用户名',max_length=255, unique=True, )
    password = models.CharField(verbose_name='密码', max_length=128)
    name = models.CharField('名字', max_length=32)
    school = models.CharField('学校', max_length=32)
    birthday = models.DateField(verbose_name='生日')
    mobile = models.CharField('手机', max_length=32, default=None, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField('Role', verbose_name='用户角色', blank=True, null=True, default=2)

    def __str__(self):
        return "{}".format(self.username)

# 留言
class user_liuyan(models.Model):
    user = models.ForeignKey(to='UserInfo', to_field='id', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
# 公告
class annunciate(models.Model):
    msg = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
# 用户收藏
class BookList(models.Model):
    id = models.AutoField(primary_key=True)
    order_num = models.IntegerField( blank=False, null=False)
    course = models.CharField("课程名称", max_length=20)
    school = models.CharField('学校', max_length=20)
    teacher = models.CharField('主讲人', max_length=20)
    stu_num = models.IntegerField(null=True, blank=True) # 学生人数
    introduction = models.CharField(max_length=255, null=True, blank=True) # 简介
    link = models.CharField('网址', max_length=255) # 网址连接
    commend = models.IntegerField(default=0) # 推荐次数
    join_time = models.DateTimeField(auto_now_add=True)
    userinfos = models.ForeignKey(to='UserInfo', to_field='id', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.course)

    class Meta:
        unique_together = ('course', 'userinfos',)



