from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from const import db_query

# Bazani asosiy klassi (Djangodagi models.Model ga o‘xshaydi)
Base = declarative_base()

# Users modeli
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    ism = Column(String(50), nullable=False)
    familya = Column(String(50), nullable=False)
    telegram_id = Column(String(20), nullable=False, unique=True)

# MySQL ulanish
engine = create_engine(db_query, echo=True)

# Session yaratish
SessionLocal = sessionmaker(bind=engine)



def insert(ism:String, familya:String,telegram_id:String):
    try:

        session = SessionLocal()
        new_user = User(ism=ism, familya=familya, telegram_id=telegram_id)
        session.add(new_user)
        session.commit()
        session.close()
        return "ok"
    except:
        return 'Siz allaqachon testga tayyorsiz'


def delete(telegram_id:String):
    session = SessionLocal()

    foydalanuvchi = session.query(User).filter(User.telegram_id == telegram_id).delete(synchronize_session=False)
    session.commit()
    print("✅ Foydalanuvchi o‘chirildi.")

def get_all_user():

    session = SessionLocal()
    all_users = session.query(User).all()
    session.close()

    return all_users

def delete_all():
    session = SessionLocal()
    session.query(User).delete()
    session.commit()
    session.close()