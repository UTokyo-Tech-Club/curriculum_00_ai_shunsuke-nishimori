# api/models/task.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    query = Column(String(1024))   # ユーザーからのリクエスト内容
    result = Column(String(4096))   # モデル実行結果（晩御飯提案）
    done = relationship("Done", back_populates="task", cascade="delete")

class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    task = relationship("Task", back_populates="done")