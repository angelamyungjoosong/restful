from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine
# pip install sqlalchemy-utils
# pip install passlib
from sqlalchemy_utils.types.password import PasswordType
"""
sqlalchemy_utils 모둘을 추가 설치하여 PasswordType 타입 사용
PasswordType 타입은 필드에 입력된 데이터를 암호화 처리
"""

engine = create_engine('sqlite:///tmp/test.db', echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    # (3)
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    passward: Mapped[PasswordType] = mapped_column(PasswordType(
        schemes=['pbkdf2_sha512','md5_crypt'],
        deprecated=['md5_crypt']))

    def __init__(self, name=None, password=None):
        self.name = name
        self.passward = password

    def __repr__(self):
        return f'<name : {self.name}>'

def init_db():
    Base.metadata.create_all(bind=engine)