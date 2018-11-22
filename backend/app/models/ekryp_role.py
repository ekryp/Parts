from flask_security import RoleMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship, backref

from app.models.basemodel import BaseModel


class Role(BaseModel, RoleMixin):
    __tablename__ = 'ekryp_role'

    ekryp_partner_id = Column(Integer, ForeignKey('ekryp_partner.id'))
    role_name = Column(String(250))
    parent_role_id  = Column(Integer)
    description = Column(String(250))

    def __init__(self, ekryp_partner_id, role_name, parent_role_id, description):
        self.ekryp_partner_id = ekryp_partner_id if ekryp_partner_id else 0
        self.role_name = role_name
        self.parent_role_id = parent_role_id if parent_role_id else 0
        self.description = description