from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine

from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from const import db_query
import random

Base = declarative_base()

engine = create_engine(db_query, echo=False)
class Question(Base):
    __tablename__ = 'savollar'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)

    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = 'variantlar'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey('savollar.id'))
    question = relationship("Question", back_populates="options")


def set_test(data):

    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Jadvalni tozalash
    session.query(Option).delete()     # Avval foreign key jadval tozalanadi
    session.query(Question).delete()
    session.commit()

    # 2. Yangi ma’lumotlarni kiritish
    for item in data:
        q = Question(text=item["question"])
        for opt in item["options"]:
            o = Option(text=opt["text"], is_correct=opt["is_correct"])
            q.options.append(o)
        session.add(q)

    session.commit()
    session.close()

    print("✅ Barcha savollar va variantlar bazaga muvaffaqiyatli yuklandi.")

def get_test(number:int):
    engine = create_engine(db_query, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    # 1. Barcha savollarni olish
    all_questions = session.query(Question).all()

    # 2. Savollar sonini tekshirish
    if len(all_questions) < number:
        session.close()
        raise ValueError(f"❌ Bazada faqat {len(all_questions)} ta savol mavjud, lekin {number} ta so‘ralgan.")

    # 3. Tasodifiy savollarni tanlab olish
    selected_questions = random.sample(all_questions, number)

    #session.close()
    return selected_questions

