from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_session():
    return db.session



class BaseModel(db.Model):

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8', mysql_engine='InnoDB')

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(),
                            onupdate=func.now())