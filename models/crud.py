from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *
from sqlalchemy import or_, and_


def get_user(db: Session, user_id: int):
    """
    获取用户
    :param db:
    :param user_id:
    :return:
    """
    return db.query(User).filter(User.id == user_id, User.status == False).first()


def db_create_user(db: Session, user: UserCreate):
    """
    新建用户
    :param db:
    :param user:
    :return:
    """
    roles = db.query(Role).filter(Role.name == user.role).first()
    db_user = User(**user.dict())
    db_user.role = roles.id
    db.add(db_user)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_user)  # 刷新
    return db_user


def get_user_username(db: Session, username: str):
    """
    获取用户名
    :param db:
    :param username:
    :return:
    """
    return db.query(User).filter(User.username == username, User.status == False).first()


def get_role_name(db: Session, id: id):
    """
    获取角色名称
    :param db:
    :param id:
    :return:
    """
    return db.query(Role).filter(Role.id == id).first()


def get_message(db: Session, message: int):
    """
    查看留言
    :param db:
    :param message:
    :return:
    """
    return db.query(Message).filter(Message.id == message, Message.status == False).first()


def get_pid_message(db: Session, message: int):
    return db.query(Message).filter(and_(Message.id != message, Message.pid == message, Message.status == False)).all()


def get_message_list(db: Session, userid: int):
    return db.query(Message).filter(
        or_(Message.senduser == userid, Message.acceptusers == userid,
            Message.status == 0)).all()


def db_creat_rebackmessage(db: Session, reback: RebackMessConnet, senduser: int):
    """
    回复留言
    :param db:
    :param reback:
    :param senduser:
    :return:
    """
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    reabck = Message(**reback.dict())
    reabck.sendtime = times
    reabck.senduser = senduser
    db.add(reabck)
    db.commit()  # 提交保存到数据库中
    db.refresh(reabck)  # 刷新
    return reabck


def db_create_course(db: Session, course: Courses, user: int):
    """
    创建课程
    :param db:
    :param course:
    :param user:
    :return:
    """
    course = Course(**course.dict())
    course.owner = user
    db.add(course)
    db.commit()  # 提交保存到数据库中
    db.refresh(course)  # 刷新
    return course


def db_get_course_name(db: Session, name: str):
    """
    根据课程名称获取
    :param db:
    :param name:
    :return:
    """
    return db.query(Course).filter(Course.name == name, Course.status == False).first()


def db_get_course_id(db: Session, id: int):
    """
    获取课程
    :param db:
    :param id:
    :return:
    """
    return db.query(Course).filter(Course.id == id, Course.status == False).first()


def db_get_coursecomment_id(db: Session, id: int):
    return db.query(Commentcourse).filter(Commentcourse.course == id, Commentcourse.status == False).all()


def createcomments(db: Session, cousecoment: Coursecomment, user: id):
    """
    创建评论
    :param db:
    :param cousecoment:
    :param user:
    :return:
    """
    comments = Commentcourse(**cousecoment.dict())
    comments.users = user
    db.add(comments)
    db.commit()
    db.refresh(comments)
    return comments


def get_cousecomments(db: Session, id: int):
    return db.query(Commentcourse).filter(Commentcourse.id == id, Commentcourse.status == False).all()


def get_student(db: Session, couese: int, user: int):
    """
    获取学生
    :param db:
    :param couese:
    :param user:
    :return:
    """
    return db.query(Studentcourse).filter(Studentcourse.course == couese, Studentcourse.students == user,
                                          Studentcourse.status == True).first()


def add_student_course(db: Session, couese: int, user: int):
    studentcourse = Studentcourse(students=couese,
                                  course=user)
    db.add(studentcourse)
    db.commit()
    db.refresh(studentcourse)
    return studentcourse


def rebck_couses(db: Session, student: Studentcourse):
    """
    退出课程
    :param db:
    :param student:
    :return:
    """
    student.status = True
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def getallcourse(db: Session):
    """
    课程列表
    :param db:
    :return:
    """
    return db.query(Course).filter(Course.status == True).all()


def get_student_all(db: Session, user: int):
    """
    获取学生的课程列表
    :param db:
    :param user:
    :return:
    """
    return db.query(Studentcourse).filter(Studentcourse.students == user,
                                          Studentcourse.status == False).all()


def getlikeCourse(db: Session):
    """
    推荐课程模型
    :param db:
    :return:
    """
    return db.query(Course).filter(Course.likenum > 500,
                                   Course.onsale == True).all()
