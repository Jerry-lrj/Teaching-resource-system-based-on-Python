import pymysql

from bysj import models


model = models.BookList.objects.all()
print(model)

# BookList中的字段:

# order_num  course    school    teacher   stu_num    introduction   link    commend

# {'order_num': source, 'course': 'Office高级应用', 'school': '成都信息工程大学', 'teacher': '黄天羽', 'start_time': '进行至第3周',
# 'stu_num': 59568, 'introduction': '本课程以全国计算机等级考试“二级MS Office高级应用”考试大纲为基础，结合日常办公应用需求而有所扩展，讲解最常用的Word、Excel、PowerPoint三个应用组件，让学习者较系统地掌握Office的科学用法，在实…',
# 'link': 'http://www.icourse163.org/course/CUIT-1002260004', 'id': 1002260004, 'commend': 0}

# {'order_num': 2, 'course': '数据结构', 'school': '浙江大学', 'teacher': '礼欣', 'start_time': '进行至第3周',
# 'stu_num': 108218, 'introduction': '学了一门编程语言不知道能干啥？来学数据结构就对啦！ 学会编程相当于会砌猪圈的泥瓦匠，学完数据结构就会盖个双层小楼啦~ 同时还可以一窥构筑摩天大厦的奇门武功！ 欢迎勤奋的小白活泼乱入！十周修炼，得…',
# 'link': 'http://www.icourse163.org/course/ZJU-93001', 'id': 93001, 'commend': 0}

# {'order_num': 3, 'course': '大学计算机', 'school': '北京理工大学', 'teacher': '张伟利', 'start_time': '进行至第5周',
#  'stu_num': 50987, 'introduction': '人类在探寻自动计算奥秘的过程中，催生了计算机科学的诞生与计算技术的革命。大学计算机课程是以计算机原理和概念为基础，以计算机科学新技术新方法为主要内容，以计算思维、创新思维能力培养为目标，力求…',
# 'link': 'http://www.icourse163.org/course/BIT-47004', 'id': 47004, 'commend': 0}
