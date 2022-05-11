from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import EVENT

if EVENT == 'test':
    # 测试环境
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
else:
    # dev环境
    SQLALCHEMY_DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding='utf8',
    echo=True,
    connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()