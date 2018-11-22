from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, backref

from app.models.basemodel import BaseModel


class EkrypPartner(BaseModel):
    __tablename__ = "ekryp_partner"

    partner_name = Column(String(250))
    industry = Column(String(250))
    target_market_segment = Column(String(250))
    country = Column(String(250))
    geo = Column(String(250))
    status = Column(Boolean)
    users = relationship("User" , backref=backref("users", cascade="all"), lazy="dynamic")
    druid_datasources = relationship("DruidDatasource" , backref=backref("druid_datasources",cascade="all"), lazy="dynamic")
    roles = relationship("Role", backref=backref("roles", cascade="all"), lazy="dynamic")

    def __init__(self,id, partner_name, industry,target_market_segment, country, geo,status):
        self.id = id
        self.partner_name = partner_name
        self.industry = industry
        self.target_market_segment = target_market_segment
        self.country = country
        self.geo = geo
        self.status = status if status else True

