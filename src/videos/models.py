from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from src.auth.models import User
metadata = MetaData()

video = Table(
	'video',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('title', String),
	Column('description', String),
	Column('file', String),
	Column('user', Integer, ForeignKey(User.id)),
)

