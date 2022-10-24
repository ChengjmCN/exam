from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time


class Teachers(BaseModel):
    id: int
    name: str


class Students(BaseModel):
    id: int
    name: str


class Papers(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    duration: str
    teacher_id: Optional[int]
    lesson_id: Optional[int]


class PapersEdit(Papers):
    id: int


class PaperDetail(Papers):
    id: int
    questions: List = []


class Questions(BaseModel):
    name: str
    type: int
    paper_id: Optional[int]


class Choices(BaseModel):
    A: Optional[str]
    B: Optional[str]
    C: Optional[str]
    D: Optional[str]
    answer: str
    score: int


class ChoiceDetail(Choices):
    name: str
    type: int


class TrueFalses(BaseModel):
    answer: bool
    score: int


class TrueFalseDetail(TrueFalses):
    name: str
    type: int = 3
