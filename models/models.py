from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from datetime import datetime

from models.database import Base, engine


class User(Base):
    '''用户基础表'''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=32), unique=True, index=True)  # 用户名
    password = Column(String(length=252))  # 密码
    status = Column(Integer, default=0)  # 1.删除,0正常
    jobnum = Column(Integer, nullable=True)  # 工号
    studentnum = Column(Integer, nullable=True)  # 学号
    age = Column(Integer)  # 年龄
    sex = Column(String(length=8), default="男")  # 性别
    role = Column(Integer)  # 角色
    addtime = Column(DateTime, default=datetime.now())


class Role(Base):
    '''角色表'''
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=8), unique=True, index=True)  # 角色名称


class Course(Base):
    '''课程表'''
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=252), unique=True, index=True)  # 课程名称
    icon = Column(String(length=252), nullable=True)  # icon
    desc = Column(String(length=252), nullable=True)  # 描述
    status = Column(Boolean, default=False)  # 状态
    onsale = Column(Boolean, default=False)  # 是否上架
    catalog = Column(Text, nullable=True)  # 目录
    owner = Column(Integer, ForeignKey('users.id'))  # 拥有者
    likenum = Column(Integer, default=0)  # 点赞数


class Studentcourse(Base):
    '''学生课程表'''
    __tablename__ = "studentcourses"
    id = Column(Integer, primary_key=True, index=True)
    students = Column(Integer, ForeignKey('users.id'))  # 学生
    course = Column(Integer, ForeignKey('courses.id'))  # 课程
    addtime = Column(DateTime, default=datetime.now())  # 加入时间
    updatetime = Column(DateTime, default=addtime)  # 更新时间
    status = Column(Integer, default=0)  # 1.删除,0正常


class Commentcourse(Base):
    '''课程评论'''
    __tablename__ = "commentcourses"
    id = Column(Integer, primary_key=True, index=True)
    course = Column(Integer, ForeignKey('courses.id'))  # 课程id
    users = Column(Integer, ForeignKey('users.id'))  # 评论人
    pid = Column(Integer)  # 回复。
    addtime = Column(DateTime, default=datetime.now())  # 添加时间
    top = Column(Boolean, default=False)  # 是否置顶
    context = Column(Text)
    status = Column(Integer, default=0)  # 1.删除,0正常


class Message(Base):
    '''消息表'''
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    senduser = Column(Integer, ForeignKey('users.id'))  # 发送者
    acceptusers = Column(Integer, ForeignKey('users.id'))  # 接受者
    read = Column(Boolean, default=False)  # 是否已读，接受者是否已读
    sendtime = Column(String(length=252))  # 发送时间
    pid = Column(Integer)
    addtime = Column(DateTime, default=datetime.now())  # 添加时间
    context = Column(Text)
    status = Column(Integer, default=0)  # 1.删除,0正常


Base.metadata.create_all(bind=engine)