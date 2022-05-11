from models.database import *


def get_db_pro():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db = get_db_pro