from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    """
    基本模型
    """
    username: str


class UserCreate(UserBase):
    """
    请求模型验证：
    username:
    password:
    """
    password: str
    role: int
    jobnum: Optional[int] = None
    studentnum: Optional[int] = None
    sex: str = "男"
    age: int


class UserLogin(UserBase):
    """
    密码模型
    """
    password: str


class UserToken(BaseModel):
    """
    token模型
    """
    token: str


class UsernameRole(UserBase):
    """
    用户角色模型
    """
    role: str


class UserChangepassword(BaseModel):
    """
    修改密码模型
    """
    password: str
    newpassword: str


class MessageConent(BaseModel):
    """
    留言模型
    """
    id: int
    connect: str


class Messages(BaseModel):
    """
    查看留言模型
    """
    id: int
    senduser: str
    acceptusers: str
    read: bool
    sendtime: str
    addtime: str
    context: str


class MessagePid(Messages):
    """
    查看留言模型
    """
    pid: int


class MessageOne(Messages):
    """
    查看留言模型
    """
    pid: List[MessagePid] = []


class RebackMessConnet(MessageConent):
    """
    回复留言模型
    """
    rebackid: int


class Courses(BaseModel):
    """
    课程模型
    """
    name: str
    icon: Optional[str]
    desc: Optional[str]
    catalog: Optional[str]
    onsale: Optional[int]
    owner: str
    likenum: int


class CoursesCommentBase(BaseModel):
    users: str
    pid: int
    addtime: str
    context: str


class Coursescomment(CoursesCommentBase):
    id: int
    top: int


class CousesDetail(Courses):
    id: int
    commonet: List[Coursescomment] = []


class CoursesEdit(Courses):
    id: int


class Coursecomment(BaseModel):
   id: int
   comments: str
   pid: Optional[int]