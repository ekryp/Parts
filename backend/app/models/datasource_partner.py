from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.models.basemodel import BaseModel


class DatasourcePartner(BaseModel):
    __tablename__ = 'datasource_partner'

    ekryp_partner_id = Column(Integer, ForeignKey('ekryp_partner.id'))
    ekryp_datasource_id = Column(Integer, ForeignKey('druid_datasources.id'))
    datasource_key = Column(String(25+0))