from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from src.auth.models import user

metadata = MetaData()

video = Table(
	'video',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('title', String(100), nullable=False),
	Column('description', String(200), default=None),
	Column('preview', String),
	Column('file', String),
	Column('user_id', Integer, ForeignKey(user.c.id, ondelete='CASCADE')),
)
