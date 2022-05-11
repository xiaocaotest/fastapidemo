from fastapi import APIRouter, Depends, Request
from models.crud import *
from models.get_db import get_db
from routers.user import get_cure_user
from common.jsontools import reponse
from fastapi.encoders import jsonable_encoder

courseRouter = APIRouter()


@courseRouter.post(path='/create')
async def create(coursescreate: Courses,
                 db: Session = Depends(get_db), user: UsernameRole = Depends(get_cure_user)):
    """
    创建课程
    :param coursescreate:
    :param db:
    :param user:
    :return:
    """
    user_ = get_user_username(db, user.username)
    user_role = get_role_name(db, user_.role)
    if not user_role or user_role.mame == "学生":
        return reponse(code=101004, message='只有老师才能创建课程', data='只有老师才能创建课程')
    if len(coursescreate.name) > 50 or len(coursescreate.name) < 2:
        return reponse(code=101005, message='课程名长度应该在2-50', data='')
    if coursescreate.onsale != 0 or coursescreate.onsale != 1:
        return reponse(code=101006, message='课程上架状态不对', data='')
    name = db_get_course_name(db, coursescreate.name)
    if name:
        return reponse(code=101002, message='课程名称不能重复', data='课程名称不能重复')
    couse = db_create_course(db, coursescreate, user_.id)
    return reponse(code=200, message='成功', data=couse)


@courseRouter.get(path='/detail/{id}')
async def detail(id: int,
                 db: Session = Depends(get_db)):
    """
    获取课程评论
    :param id:
    :param db:
    :return:
    """
    course = db_get_course_id(db, id)
    if course:
        coursedetail = CousesDetail(id=course.id,
                                    name=course.name,
                                    icon=course.icon, desc=course.desc, catalog=course.catalog,
                                    onsale=course.onsale, owner=get_user(db, course.owner).username,
                                    likenum=course.likenum)
        allcomments = db_get_coursecomment_id(db, course.id)
        all_comments_list = []
        if len(allcomments) > 0:
            for item in allcomments:
                detailcomment = Coursescomment(id=item.id,
                                               top=item.top,
                                               users=get_user(db, item.users).username,
                                               pid=item.id, addtime=str(item.addtime),
                                               context=item.context)
                all_comments_list.append(detailcomment)
        coursedetail.commonet = all_comments_list
        return reponse(code=200, message='成功', data=jsonable_encoder(coursedetail))
    return reponse(code=200, message="成功", data='')


@courseRouter.put(path='/edit')
async def edit(
        coursesedit: CoursesEdit,
        db: Session = Depends(get_db), user: UsernameRole = Depends(get_cure_user)):
    """
    添加评论
    :param coursesedit:
    :param db:
    :param user:
    :return:
    """
    users = get_user_username(db, user.username)
    couses_is = db_get_course_id(db, coursesedit.id)
    if not couses_is:
        return reponse(code=101201, data='', message='课程id不存在')
    couses_name = db_get_course_name(db, coursesedit.name)
    if couses_name:
        return reponse(code=101203, data='', message='课程名称不能重复')
    if couses_is.owner == users.id:
        couses_is.catalog = coursesedit.catalog
        couses_is.desc = coursesedit.desc
        couses_is.icon = coursesedit.icon
        couses_is.name = coursesedit.name
        db.commit()
        db.refresh(couses_is)
        return reponse(code=200, message='成功', data=couses_is)
    return reponse(code=101202, message='权限不足', data='')


@courseRouter.get(path='/viewcomments/{id}')
async def viewcomments(id: int,
                       db: Session = Depends(get_db)):
    """
    查看评论接口
    :param id:
    :param db:
    :return:
    """
    couses = db_get_course_id(db, id)
    if couses:
        allcomments = db_get_coursecomment_id(db, couses.id)
        all_comments_list = []
        if len(allcomments) > 0:
            for item in allcomments:
                detailcomment = Coursescomment(id=item.id,
                                               top=item.top,
                                               users=get_user(db, item.users).username,
                                               pid=item.id, addtime=str(item.addtime),
                                               context=item.context)
                all_comments_list.append(detailcomment)
        return reponse(code=200, message="成功", data=jsonable_encoder(all_comments_list))
    return reponse(code=101301, message='课程id不存在', data='')


@courseRouter.post(path="/comments")
async def comments(comments: Coursecomment,
                   user: UsernameRole = Depends(get_cure_user),
                   db: Session = Depends(get_db)):
    """
    评论接口
    :param comments:
    :param user:
    :param db:
    :return:
    """
    if comments.comments == '':
        return reponse(code=101402, message='评论内容不能为空', data='')
    users = get_user_username(db, user.username)
    couses = db_get_course_id(db, comments.id)
    if couses:
        if couses.owner == users.id and comments.pid is None:
            return reponse(code=101404, message='自己不能评论自己的课程', data='')
        if comments.pid is not None:
            pid_course = get_cousecomments(db, comments.pid)
            if pid_course:
                createcomments(db, comments, users.id)
                return reponse(code=200, message='成功', data='')
            return reponse(code=101405, message='回复的评论不存在', data='')
        createcomments(db, comments, users.id)
        return reponse(code=200, message='成功', data='')
    return reponse(code=101401, message='课程id不存在', data='')


@courseRouter.get(path='/add/{id}')
async def add(id: int, user: UsernameRole = Depends(get_cure_user),
              db: Session = Depends(get_db)):
    """
    加入课程接口
    :param id:
    :param user:
    :param db:
    :return:
    """
    users = get_user_username(db, user.username)
    if user.role == '教师':
        return reponse(code=101503, message="老师不能加入课程", data='')
    couses = db_get_course_id(db, id)
    if not couses:
        return reponse(code=101501, message='课程id不存在', data='')
    userstudent = get_student(db, couses.id, users.id)
    if userstudent:
        return reponse(code=101502, message='课程不能重复加入', data='')
    reslut = add_student_course(db, couses.id, users.id)
    return reponse(code=200, message='成功', data=reslut.id)


@courseRouter.get(path='/quit/{id}')
async def quit(id: int, user: UsernameRole = Depends(get_cure_user),
               db: Session = Depends(get_db)):
    """
    退出课程接口
    :param id:
    :param user:
    :param db:
    :return:
    """
    users = get_user_username(db, user.username)

    if user.role == "老师":
        return reponse(code=101603, message='老师不能退出课程', data='')
    couses = get_student(db, id, users.id)
    if not couses:
        return reponse(code=101602, message='课程不在自己列表', data='')
    reslut = rebck_couses(db, couses)
    return reponse(code=200, message='成功', data=reslut.id)


@courseRouter.get("/list")
async def list(db: Session = Depends(get_db)):
    """
    查看课程列表
    :param db:
    :return:
    """
    allcouese = getallcourse(db)
    all_course = []
    if len(allcouese) > 0:
        for item in allcouese:
            coursedetail = CousesDetail(id=item.id,
                                        name=item.name,
                                        icon=item.icon, desc=item.desc, catalog=item.catalog,
                                        onsale=item.onsale, owner=get_user(db, item.owner).username,
                                        likenum=item.likenum)
            all_course.append(coursedetail)
    return reponse(code=200, message='成功', data=jsonable_encoder(all_course))


@courseRouter.get("/courselist")
async def courselist(user: UsernameRole = Depends(get_cure_user), db: Session = Depends(get_db)):
    if user.role == "教师":
        return reponse(code=200, message='成功', data='')

    users = get_user_username(db, user.username)

    allconut = get_student_all(db, users.id)
    all_course = []
    if len(allconut) > 0:
        for item in allconut:
            one = db_get_course_id(db, item.course)
            coursedetail = CousesDetail(id=one.id,
                                        name=one.name,
                                        icon=one.icon, desc=one.desc, catalog=one.catalog,
                                        onsale=one.onsale, owner=get_user(db, one.owner).username,
                                        likenum=one.likenum)
            all_course.append(coursedetail)
    return reponse(code=200, message='成功', data=jsonable_encoder(all_course))


@courseRouter.get("/recommend")
async def recommend(db: Session = Depends(get_db)):
    """
    推荐课程接口
    :param db:
    :return:
    """
    allcouese = getlikeCourse(db)
    all_course = []
    if len(allcouese) > 0:
        for item in allcouese:
            coursedetail = CousesDetail(id=item.id,
                                        name=item.name,
                                        icon=item.icon, desc=item.desc, catalog=item.catalog,
                                        onsale=item.onsale, owner=get_user(db, item.owner).username,
                                        likenum=item.likenum)
            all_course.append(coursedetail)
    return reponse(code=200, message='成功', data=jsonable_encoder(all_course))


@courseRouter.get("/like/{id}")
async def like(rquest: Request, id: int, user: UsernameRole = Depends(get_cure_user), db: Session = Depends(get_db)):
    """
    课程点赞接口
    :param rquest:
    :param id:
    :param user:
    :param db:
    :return:
    """
    course = db_get_course_id(db, id)
    if not course:
        return reponse(code=102001, message='课程不存在', data='')
    result = await rquest.app.state.redis.hgetall(str(course.id) + "_like", encoding='utf8')
    if user.username in result.keys():
        return reponse(code=102002, message='已经点赞，不能重复点赞', data='')
    username = user.username
    rquest.app.state.redis.hmset_dict(str(course.id) + "_like", username=username)
    course.likenum += 1
    db.commit()
    db.refresh(course)
    return reponse(code=200, message='成功', data=course.id)


@courseRouter.get(path="/onshelf/{id}")
async def offshelf(id: int, user: UsernameRole = Depends(get_cure_user),
                   db: Session = Depends(get_db)):
    """
    课程上架
    :param id:
    :param user:
    :param db:
    :return:
    """
    users = get_user_username(db, user.username)
    if user.role == "学生":
        return reponse(code=102104, message='权限不足', data='')
    couses = db_get_course_id(db, id)
    if not couses:
        return reponse(code=102101, message='课程不存在', data='')
    if couses.onsale is True:
        return reponse(code=102102, message='课程已经上架', data='')
    if couses.owner != users.id:
        return reponse(code=102103, message='自己只能上架自己的课程', data='')
    couses.onsale = True
    db.commit()
    db.refresh(couses)
    return reponse(code=200, message='成功', data=couses.id)


@courseRouter.get(path="/offshelf/{id}")
async def offshelf(id: int, user: UsernameRole = Depends(get_cure_user),
                   db: Session = Depends(get_db)):
    """
    课程下架
    :param id:
    :param user:
    :param db:
    :return:
    """
    users = get_user_username(db, user.username)
    if user.role == "学生":
        return reponse(code=102204, message='权限不足', data='')
    couses = db_get_course_id(db, id)
    if not couses:
        return reponse(code=102201, message='课程不存在', data='')
    if couses.onsale is False:
        return reponse(code=102202, message='课程已经下架', data='')
    if couses.owner != users.id:
        return reponse(code=102203, message='自己只能下架自己的课程', data='')
    couses.onsale = False
    db.commit()
    db.refresh(couses)
    return reponse(code=200, message='成功', data=couses.id)
