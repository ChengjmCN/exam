from fastapi import APIRouter, Depends, Request, Query
from fastapi.encoders import jsonable_encoder
from models.get_db import get_db
from common.resinfo import response
from models.crud import *

paperRouter = APIRouter()


# 创建试卷
@paperRouter.post(path='/paper/create', summary='创建试卷')
async def create(paper_create: Papers,
                 teacher_id: int = Query(...),
                 lesson_id: int = Query(...),
                 db: Session = Depends(get_db)):
    name = db_get_paper_name(db, paper_create.name)
    if name:
        return response(code=100101, message='试卷名称不能重复', data='')
    paper = db_create_paper(db, paper_create, teacher_id, lesson_id)
    return response(code=200, message='创建试卷成功', data=jsonable_encoder(paper))


# 编辑试卷
@paperRouter.put(path='/paper/edit', summary='编辑试卷')
async def edit(paper_edit: PapersEdit,
               teacher_id: int,
               db: Session = Depends(get_db)):
    paper_cur = db_get_paper_id(db, paper_edit.id)
    if not paper_cur:
        return response(code=100103, message='试卷不存在', data='')
    paper_name = db_get_paper_name(db, paper_edit.name)
    if paper_name and paper_name.name != paper_edit.name:
        return response(code=100101, message='试卷名称不能重复', data='')
    if paper_cur.teacher_id != teacher_id:
        return response(code=100104, message='没有权限', data='')
    paper_cur.name = paper_edit.name
    paper_cur.start_time = paper_edit.start_time
    paper_cur.end_time = paper_edit.end_time
    paper_cur.duration = paper_edit.duration
    # paper_cur.lesson_id = paper_edit.lesson_id
    db.commit()
    db.refresh(paper_cur)
    return response(code=200, message='修改试卷成功', data=jsonable_encoder(paper_cur))


# 删除试卷
@paperRouter.get(path='/paper/delete', summary='删除试卷')
async def delete(paper_id: int,
                 teacher_id: int,
                 db: Session = Depends(get_db)):
    paper_cur = db_get_paper_id(db, paper_id)
    if not paper_cur:
        return response(code=100103, message='试卷不存在', data='')
    if paper_cur.teacher_id != teacher_id:
        return response(code=100104, message='没有权限', data='')
    paper_cur.status = 2
    db.commit()
    db.refresh(paper_cur)
    return response(code=200, message='删除试卷成功', data='')


# 发布试卷
@paperRouter.get(path='/paper/publish', summary='发布试卷')
async def publish(paper_id: int,
                  teacher_id: int,
                  db: Session = Depends(get_db)):
    paper_cur = db_get_paper_id(db, paper_id)
    if not paper_cur:
        return response(code=100103, message='试卷不存在', data='')
    if paper_cur.teacher_id != teacher_id:
        return response(code=100104, message='没有权限', data='')
    paper_cur.status = 1
    db.commit()
    db.refresh(paper_cur)
    return response(code=200, message='发布试卷成功', data='')


# 试卷详情
@paperRouter.get(path='/paper/detail', summary='试卷详情')
async def detail(paper_id: int,
                 teacher_id: int,
                 db: Session = Depends(get_db)):
    paper_cur = db_get_paper_id(db, paper_id)
    if not paper_cur:
        return response(code=100103, message='试卷不存在', data='')
    if paper_cur.teacher_id != teacher_id:
        return response(code=100104, message='没有权限', data='')
    paper_detail = PaperDetail(id=paper_cur.id,
                               name=paper_cur.name,
                               add_time=paper_cur.add_time,
                               start_time=paper_cur.start_time,
                               end_time=paper_cur.end_time,
                               duration=paper_cur.duration,
                               lesson_id=paper_cur.lesson_id,
                               teacher_id=paper_cur.teacher_id)
    questions = db_get_question_paper_id(db, paper_id)
    for question in questions:
        if question.type == 1 or question.type == 2:
            question_info = db_get_choice(db, question.id)
            question_ans = ChoiceDetail(name=question.name, type=question.type,
                                        A=question_info.A, B=question_info.B,
                                        C=question_info.C, D=question_info.D,
                                        answer=question_info.answer, score=question_info.score)
        if question.type == 3:
            question_info = db_get_truefalse(db, question.id)
            question_ans = TrueFalseDetail(name=question.name, type=question.type,
                                           answer=question_info.answer, score=question_info.score)
        paper_detail.questions.append(question_ans)
    return response(code=200, message='成功', data=jsonable_encoder(paper_detail))


# 试卷列表(老师)
@paperRouter.get(path='/paper/list', summary='试卷列表(老师)')
async def get_list(teacher_id: int,
                   db: Session = Depends(get_db)):
    teacher = db_get_teacher_id(db, teacher_id)
    if not teacher:
        return response(code=200, message='该教师不存在', data='')
    paper_curs = db_get_papers_teacher(db, teacher_id)
    paper_list = []
    if len(paper_curs) > 0:
        for paper_cur in paper_curs:
            paper_detail = PaperDetail(id=paper_cur.id,
                                       name=paper_cur.name,
                                       add_time=paper_cur.add_time,
                                       start_time=paper_cur.start_time,
                                       end_time=paper_cur.end_time,
                                       duration=paper_cur.duration,
                                       lesson_id=paper_cur.lesson_id)
            paper_list.append(paper_detail)
    return response(code=200, message='成功', data=jsonable_encoder(paper_list))


# 创建题目
@paperRouter.post(path='/question/create', summary='创建题目')
async def question_create(paper_id: int,
                          question_new: Questions,
                          db: Session = Depends(get_db)):
    name = db_get_question_name(db, question_new.name)
    if name:
        return response(code=100201, message='题目名称不能重复', data='')
    question = db_create_question(db, question_new, paper_id)
    return response(code=200, message='创建题目成功', data=jsonable_encoder(question))


# 创建选择题
@paperRouter.post(path='/question/choice', summary='创建选择题')
async def choice_create(question_id: int,
                        choice_new: Choices,
                        db: Session = Depends(get_db)):
    choice = db_create_choice(db, choice_new, question_id)
    return response(code=200, message='创建选择题成功', data=jsonable_encoder(choice))


# 创建判断题
@paperRouter.post(path='/question/truefalse', summary='创建判断题')
async def truefalse_create(question_id: int,
                           truefalse_new: TrueFalses,
                           db: Session = Depends(get_db)):
    truefalse = db_create_truefalse(db, truefalse_new, question_id)
    return response(code=200, message='创建判断题成功', data=jsonable_encoder(truefalse))


# 编辑选择题
@paperRouter.put(path='/question/edit/choice', summary='编辑选择题')
async def question_edit_choice(question_id: int,
                               question_edit: Choices,
                               db: Session = Depends(get_db)):
    question = db_get_question_id(db, question_id)
    if not question:
        return response(code=100202, message='题目不存在', data='')
    if question.type != 1 and question.type != 2:
        return response(code=200, message='题目类型不正确', data='')
    question_info = db_get_choice(db, question_id)
    question_info.A = question_edit.A
    question_info.B = question_edit.B
    question_info.C = question_edit.C
    question_info.D = question_edit.D
    question_info.answer = question_edit.answer
    question_info.score = question_edit.score
    db.commit()
    db.refresh(question_info)
    return response(code=200, message='修改成功', data=jsonable_encoder(question_info))


# 编辑判断题
@paperRouter.put(path='/question/edit/truefalse', summary='编辑判断题')
async def question_edit_truefalse(question_id: int,
                                  question_edit: TrueFalses,
                                  db: Session = Depends(get_db)):
    question = db_get_question_id(db, question_id)
    if not question:
        return response(code=100202, message='题目不存在', data='')
    if question.type != 3:
        return response(code=200, message='题目类型不正确', data='')
    question_info = db_get_truefalse(db, question_id)
    question_info.answer = question_edit.answer
    question_info.score = question_edit.score
    db.commit()
    db.refresh(question_info)
    return response(code=200, message='修改成功', data=jsonable_encoder(question_info))


# 删除题目
@paperRouter.get(path='/question/delete', summary='删除题目')
async def question_delete(question_id: int, db: Session = Depends(get_db)):
    question = db_get_question_id(db, question_id)
    if not question:
        return response(code=100202, message='题目不存在', data='')
    if question.type == 1 or question.type == 2:
        question_info = db_get_choice(db, question_id)
    if question.type == 3:
        question_info = db_get_truefalse(db, question_id)
    db.delete(question_info)
    db.delete(question)
    db.commit()
    return response(code=200, message='删除成功', data='')


# 查看题目信息
@paperRouter.get(path='/question/detail', summary='查看题目')
async def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = db_get_question_id(db, question_id)
    if not question:
        return response(code=100202, message='题目不存在', data='')
    if question.type == 1 or question.type == 2:
        question_info = db_get_choice(db, question_id)
        question_ans = ChoiceDetail(name=question.name, type=question.type,
                                    A=question_info.A, B=question_info.B,
                                    C=question_info.C, D=question_info.D,
                                    answer=question_info.answer, score=question_info.score)
    if question.type == 3:
        question_info = db_get_truefalse(db, question_id)
        question_ans = TrueFalseDetail(name=question.name, type=question.type,
                                       answer=question_info.answer, score=question_info.score)
    return response(code=200, message='成功', data=jsonable_encoder(question_ans))

