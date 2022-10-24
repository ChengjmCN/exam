from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *


# 查询教师（按id）
def db_get_teacher_id(db: Session, teacher_id: int) -> Teacher:
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()


# 创建试卷
def db_create_paper(db: Session, paper: Papers, teacher_id: int, lesson_id: int) -> Paper:
    paper = Paper(**paper.dict())
    paper.teacher_id = teacher_id
    paper.lesson_id = lesson_id
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


# 查询试卷（按名称）
def db_get_paper_name(db: Session, name: str) -> Paper:
    return db.query(Paper).filter(Paper.name == name, Paper.status != 2).first()


# 查询试卷（按id）
def db_get_paper_id(db: Session, paper_id: int) -> Paper:
    return db.query(Paper).filter(Paper.id == paper_id, Paper.status != 2).first()


# 查询试卷列表（教师）
def db_get_papers_teacher(db: Session, teacher_id: int) -> Paper:
    return db.query(Paper).filter(Paper.teacher_id == teacher_id).all()


# 创建题目
def db_create_question(db: Session, question: Questions, paper_id: int) -> Question:
    question = Question(**question.dict())
    question.paper_id = paper_id
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


# 查询题目（按名称）
def db_get_question_name(db: Session, name: str) -> Question:
    return db.query(Question).filter(Question.name == name).first()


# 查询题目（按id）
def db_get_question_id(db: Session, question_id: int) -> Question:
    return db.query(Question).filter(Question.id == question_id).first()


# 查询题目（按试卷名称）
def db_get_question_paper_id(db: Session, paper_id: int) -> Question:
    return db.query(Question).filter(Question.paper_id == paper_id).all()


# 创建选择题
def db_create_choice(db: Session, choice: Choices, question_id: int) -> Choice:
    choice = Choice(**choice.dict())
    choice.question_id = question_id
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


# 查询选择题
def db_get_choice(db: Session, question_id: int) -> Choice:
    return db.query(Choice).filter(Choice.question_id == question_id).first()


# 创建判断题
def db_create_truefalse(db: Session, truefalse: TrueFalses, question_id: int) -> TrueFalse:
    truefalse = TrueFalse(**truefalse.dict())
    truefalse.question_id = question_id
    db.add(truefalse)
    db.commit()
    db.refresh(truefalse)
    return truefalse


# 查询判断题
def db_get_truefalse(db: Session, question_id: int) -> TrueFalse:
    return db.query(TrueFalse).filter(TrueFalse.question_id == question_id).first()