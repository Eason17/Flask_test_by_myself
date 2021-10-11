from flask import request
import json, re, datetime, random, os
from model import Student, Project
from werkzeug.utils import secure_filename

def get_Info(sname = None, group = None, grade = None, input = None):
    info = None
    if sname:
        sname = re.sub(' ', "", sname)  # 除去空格
        sname = re.sub('\d+', "", sname)  # 提取姓名
    # 查询数据
    if sname and group and grade:
        info = Student.query.filter(Student.SName == sname, Student.Group == group, Student.Grade == grade).all()
        if not info: # 模糊查询
            sname = "%" + sname + "%"  # 模糊条件
            info = Student.query.filter(Student.SName.like(sname)).all()
    elif sname and group:
        info = Student.query.filter(Student.SName == sname, Student.Group == group).all()
        if not info: # 模糊查询
            sname = "%" + sname + "%"  # 模糊条件
            info = Student.query.filter(Student.SName.like(sname)).all()
    elif sname and grade:
        info = Student.query.filter(Student.SName == sname, Student.Grade == grade).all()
        if not info: # 模糊查询
            sname = "%" + sname + "%"  # 模糊条件
            info = Student.query.filter(Student.SName.like(sname)).all()
    elif group and grade:
        info = Student.query.filter(Student.Group == group, Student.Grade == grade).all()
    elif sname:
        info = Student.query.filter(Student.SName == sname).all()
        if not info: # 模糊查询
            sname = "%" + sname + "%"  # 模糊条件
            info = Student.query.filter(Student.SName.like(sname)).all()
    elif group:
        info = Student.query.filter(Student.Group == group).all()
    elif grade:
        info = Student.query.filter(Student.Grade == grade).all()

    elif input:
        input = re.sub(' ', "", input)  # 除去空格
        # 输入条件为学号查询
        input_sno = re.sub('\D', "", input)  # 提取数字
        if len(input_sno) > 6:
            info = Student.query.filter(Student.SNo == input_sno).all()
            if not info:
                input_sno = "%" + input_sno + "%"
                info = Student.query.filter(Student.SNo.like(input_sno)).all()

        if not info:
            # 为姓名查询
            input_name = re.sub('\d+',"",input) # 提取姓名
            if len(input_name) >= 1: # 存在
                info = Student.query.filter(Student.SName == input_name).all()
                if not info: # 模糊查询
                    input_name = "%" + input_name + "%"
                    info = Student.query.filter(Student.SName.like(input_name)).all()

        if not info:
            # 为组别
            input_group = re.sub('\d+', "", input)  # 提取组别
            if len(input_group) >= 1:  # 存在
                info = Student.query.filter(Student.Group == input_group).all()
                if not info: # 模糊查询
                    input_group = "%" + input_group +"%"
                    info = Student.query.filter(Student.Group.like(input_group)).all()

        if not info:
            # 为年级查询
            input_grade = re.sub('\D',"",input) # 提取年级
            if 4 >= len(input_grade) >= 2:# 存在
                info = Student.query.filter(Student.Grade == input_grade).all()
                if not info:
                    input_grade = "%" + input_grade + "%"
                    info = Student.query.filter(Student.Grade.like(input_grade)).all()
        if not info:
            info = []
    return info

def to_Data():
    # data = request.get_data()  # 获取前端数据
    # data = str(data, 'utf-8')  # 转utf-8
    # data = json.loads(data)  # json转字典
    data = json.loads(request.get_data().decode("utf-8"))
    if data:
        return data
    else:
        return {}

def to_Json(list = None):
    if list:
        data = json.dumps(list, ensure_ascii = False)
    else:
        data = "0"
    return data

def to_List(info, page): # page为页数
    list = []
    limit = 10 # 限制返回数据条数
    index = len(info)  # 行索引
    for row in range(index):
        dic_stu = {
            'sno': info[row].SNo,
            'image_url':info[row].Avatar,
            'name': info[row].SName,
            'grade': info[row].Grade,
            'group': info[row].Group,
            'contact':{
                'phone': info[row].Telephone,
                'wx': info[row].WeChat,
                'qq': info[row].QQ,
                'email': info[row].MailBox,
                'other': info[row].Other
            },
            'graduation':{
                'job': info[row].Occupation,
                'address': info[row].WorkAddress,
                'study': info[row].Direction
            },
        }

        list_pro = []
        pro_info = Project.query.filter(Project.SNo == info[row].SNo).all()
        for row_ in range(len(pro_info)):
            dic_pro = {
                'ID': pro_info[row_].ID,
                'name': pro_info[row_].Project,
                'prize': pro_info[row_].Award,
                'code': pro_info[row_].Code
            }
            list_pro.append(dic_pro)
        dic_stu['project_arr'] = list_pro

        list.append(dic_stu)  # 合并

    total = limit * page

    list = list[total-limit:total]  # 切片，存储limit之外的所有数据
    return list

def new_avatar_name(avatar_name):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand_num = random.randint(10,99)  # 随机10到99
    name = secure_filename(avatar_name)
    ext = name.rsplit('.', 1)[1]  # 扩展名
    avatar_name = str(now_time) + str(rand_num) + '.' + ext  # 合成
    return avatar_name
