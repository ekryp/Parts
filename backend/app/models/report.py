from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Text

from app.models.basemodel import BaseModel


class ReportModel(BaseModel):
	__tablename__ = 'report'

	_access_type = {
		'public': 'public',
		'private': 'private'
	}
	_status = {
		'active': 'active',
		'deleted': 'deleted'
	}
	name = Column(String(255))
	meta_data = Column(Text(4294967295))
	rank = Column(Integer, default=0)
	created_by = Column(Integer, ForeignKey('ekryp_user.id'))
	access_type = Column(String(255)) 
	status = Column(String(255))
	version = Column(Integer, default=1)
	
