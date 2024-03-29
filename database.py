from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


# 유저 정보에 대한 테이블
class User(Base):
    __tablename__ = 'users'

    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    age: Mapped[int]
    # Prescription 여러개와 참조 관계를 형성
    prescrip: Mapped[List["Prescription"]] = relationship(back_populates='user', cascade='all, delete')

    def __repr__(self):
        return f'<uid : {self.uid} name : {self.name}>'

    def to_dict(self): #딕셔너리화 시켜서 리턴
        return {'uid': self.uid,
                'name': self.name,
                'email': self.email,
                'age': self.age}
# 약품 정보에 대한 테이블
class Medicine(Base):
    __tablename__ = 'medicines'

    mid: Mapped[str] = mapped_column(primary_key=True)
    name_ko: Mapped[str]
    name_en: Mapped[str]
    size: Mapped[str]
    ing_code: Mapped[str]
    ing_name: Mapped[str]
    # Prescription 여러개와 참조 관계를 형성
    prescrip: Mapped[List["Prescription"]] = relationship(back_populates='medicines', cascade='all, delete')

    def __repr__(self):
        return f'<mid : {self.mid} name : {self.name_ko}>'
    def to_dict(self):
        return {'mid': self.mid,
                'name_ko': self.name_ko,
                'name_en': self.name_en,
                'size': self.size,
                'ing_code': self.ing_code,
                'ing_name': self.ing_name}

# 유저와 약품이 연결된 처방정보에 대한 테이블
class Prescription(Base):
    __tablename__ = 'prescriptions'

    # Medicine과 User의 주키를 외래키로 가져오고 두개 키를 사용하여 주키로 활용
    mid: Mapped[str] = mapped_column(ForeignKey("medicines.mid"), primary_key=True)
    uid: Mapped[int] = mapped_column(ForeignKey("users.uid"), primary_key=True)
    date: Mapped[datetime]
    # 하나의 Medicine과 User와 참조 관계를 형성
    medicines: Mapped["Medicine"] = relationship(back_populates="prescrip")
    user: Mapped["User"] = relationship(back_populates='prescrip')

    def __repr__(self):
        return f'<mid : {self.mid} uid : {self.uid}>'

    def to_dict(self):
        return {'mid': self.mid,
                'uid': self.uid,
                'date': self.date}
def get_engine():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///tmp/ump.db', echo=False)
    Base.metadata.create_all(bind=engine)
    return engine

