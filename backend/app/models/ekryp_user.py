from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship
from passlib.apps import custom_app_context as pwd_context
from flask_security import UserMixin

from app.models.basemodel import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = 'ekryp_user'

    ekryp_partner_id = Column(Integer, ForeignKey('ekryp_partner.id'))
    first_name = Column(String(255))
    last_name = Column(String(250))
    username = Column(String(250), index=True)
    password = Column(String(250))
    email_id = Column(String(250))
    phone_no = Column(String(250))
    address = Column(String(500))
    status = Column(String(250))
    role_id = Column(Integer)
    settings = Column(String(5000), nullable=True, default=None)
    dash_settings = Column(String(5000), nullable=True, default=None)
    remember_me = Column(String(255))
    last_login_at = Column(DateTime)


    def __init__(self, ekryp_partner_id, first_name, last_name,email_id, phone_no, address,
                 role_id, settings, dash_settings):
        self.ekryp_partner_id = ekryp_partner_id if ekryp_partner_id else 0
        self.settings = settings
        self.dash_settings = dash_settings
        self.first_name = first_name
        self.last_name = last_name
        self.username = email_id
        self.email_id = email_id
        self.phone_no = phone_no
        self.address = address
        self.status = True
        self.role_id = role_id if role_id else 0


class UserSettings(BaseModel):
    __tablename__ = 'ekryp_settings'
    ekryp_user = Column(Integer, ForeignKey('ekryp_user.id'))
    name = Column(String(50), index=True)
    data = Column(String(5000))
