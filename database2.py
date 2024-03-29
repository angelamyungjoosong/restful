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
class Store(Base):
    __tablename__ = 'store_table'

    s_id: Mapped[int] = mapped_column(primary_key=True)
    locate: Mapped[str]
    name: Mapped[str]
    phone_num: Mapped[int]
    city: Mapped[str]

    # Prescription 여러개와 참조 관계를 형성
    inventory: Mapped[List["Inventory"]] = relationship(back_populates='store', cascade='all, delete')
    def __repr__(self):
        return f'<s_id : {self.s_id} name : {self.name}>'

    def to_dict(self):
        return {'s_id': self.s_id,
                'locate': self.locate,
                'name': self.locate,
                'phone_num': self.phone_num,
                'city': self.city}

# 약품 정보에 대한 테이블
class Medicine(Base):
    __tablename__ = 'medicine_table'

    m_id: Mapped[str] = mapped_column(primary_key=True)
    name_ko: Mapped[str]
    name_en: Mapped[str]
    size: Mapped[str]
    ing_code: Mapped[str]
    ing_name: Mapped[str]
    # Prescription 여러개와 참조 관계를 형성
    inventory: Mapped[List["Inventory"]] = relationship(back_populates='medicine', cascade='all, delete')

    def __repr__(self):
        return f'<m_id : {self.m_id} name : {self.name_ko}>'
    def to_dict(self):
        return {'m_id': self.m_id,
                'name_ko': self.name_ko,
                'name_en': self.name_en,
                'size': self.size,
                'ing_code': self.ing_code,
                'ing_name': self.ing_name
                }

# 유저와 약품이 연결된 처방정보에 대한 테이블
class Inventory(Base):
    __tablename__ = 'inventory_table'

    # Medicine과 User의 주키를 외래키로 가져오고 두개 키를 사용하여 주키로 활용
    m_id: Mapped[str] = mapped_column(ForeignKey("medicine_table.m_id"), primary_key=True)
    s_id: Mapped[int] = mapped_column(ForeignKey("store_table.s_id"), primary_key=True)
    manage_date: Mapped[datetime]
    price: Mapped[int]
    count: Mapped[int]
    # 하나의 Medicine과 User와 참조 관계를 형성
    medicine: Mapped["Medicine"] = relationship(back_populates="inventory")
    store: Mapped["Store"] = relationship(back_populates='inventory')

    def __repr__(self):
        return f'<m_id : {self.m_id} s_id : {self.s_id}>'
    def to_dict(self):
        return {'m_id': self.m_id,
                's_id': self.s_id,
                'manage_date': self.manage_date}
def get_engine():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///tmp/test.db', echo=False)
    Base.metadata.create_all(bind=engine)
    return engine