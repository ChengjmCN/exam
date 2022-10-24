from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Time
from datetime import datetime
from models.database import Base, engine

"""数据库模型表"""

class Student(Base):
    """学生表"""
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)    # 学号
    name = Column(String(length=30), index=True)   # 用户名
    password = Column(String(length=30))    # 密码


class Teacher(Base):
    """教师表"""
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)    # 教工号
    name = Column(String(length=30), index=True)   # 用户名
    password = Column(String(length=30))    # 密码


class Lesson(Base):
    """课程表"""
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)  # 课程id
    name = Column(String(length=30))       # 课程名称


class LessonTeacher(Base):
    """教师课程表"""
    __tablename__ = "lesson_teachers"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))     # 课程id
    teacher_id = Column(Integer, ForeignKey('teachers.id'))   # 教师id


class LessonStudent(Base):
    """学生课程表"""
    __tablename__ = "lesson_students"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))     # 课程id
    teacher_id = Column(Integer, ForeignKey('students.id'))   # 学生id


class Paper(Base):
    """试卷表"""
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), unique=True, index=True)       # 试卷名称
    status = Column(Integer, default=0)    # 试卷状态：0未发布，1已发布，2删除
    add_time = Column(DateTime, default=datetime.now())     # 添加时间
    start_time = Column(DateTime)           # 开始时间
    end_time = Column(DateTime)             # 结束时间
    duration = Column(String(length=20))    # 考试时长
    score = Column(Integer)                 # 试卷总分
    teacher_id = Column(Integer, ForeignKey('teachers.id'))    # 所属教师
    lesson_id = Column(Integer, ForeignKey('lessons.id'))               # 课程id


class Question(Base):
    """题目表"""
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)                     # 题干信息
    type = Column(Integer)               # 试题类型：1单选题，2所选题，3判断题
    paper_id = Column(Integer, ForeignKey('papers.id'))   # 所属试卷


class Choice(Base):
    """选择题信息表"""
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))    # 所属题目
    A = Column(Text)              # 选项1内容
    B = Column(Text)
    C = Column(Text)
    D = Column(Text)
    answer = Column(String(length=5))   # 答案
    score = Column(Integer)             # 分数


class TrueFalse(Base):
    """判断题题信息表"""
    __tablename__ = "truefalses"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))   # 所属题目
    answer = Column(Boolean)                 # 答案
    score = Column(Integer)                  # 分数


class Grade(Base):
    """学生成绩表"""
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    studend_id = Column(Integer, ForeignKey('students.id'))     # 所属学生
    lesson_id = Column(Integer, ForeignKey('lessons.id'))    # 课程id
    score = Column(Integer)              # 总分
    add_time = Column(DateTime, default=datetime.now())      # 添加时间


Base.metadata.create_all(bind=engine)
