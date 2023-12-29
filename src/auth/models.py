from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.orm import DeclarativeMeta, declarative_base

metadata = MetaData()

Base: DeclarativeMeta = declarative_base()

role = Table(
	'role',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String, nullable=False),
	Column("permissions", JSON),
)


class User(SQLAlchemyBaseUserTable[int], Base):

	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	username = Column(String, nullable=False, default='username')
	registered_at = Column(TIMESTAMP, default=datetime.utcnow)
	role_id = Column(Integer, ForeignKey(role.c.id))
	hashed_password: str = Column(String(length=1024), unique=True, nullable=False)
	is_active: bool = Column(Boolean, default=True, nullable=False)
	is_superuser: str = Column(Boolean, default=False, nullable=False)
	is_verified: str = Column(Boolean, default=False, nullable=False)
