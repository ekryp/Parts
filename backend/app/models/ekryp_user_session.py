from sqlalchemy import Column, String, Integer

from app.models.basemodel import BaseModel


class UserSession(BaseModel):
    __tablename__ = 'ekryp_user_session'

    access_token = Column(String(255))
    user_id = Column(Integer)
    ekryp_partner_id = Column(Integer)

    def __init__(self, access_token, user_id, ekryp_partner_id):
        self.access_token = access_token
        self.user_id = user_id
        self.ekryp_partner_id = ekryp_partner_id