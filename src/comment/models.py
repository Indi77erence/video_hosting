from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from src.auth.models import user
from src.videos.models import video

metadata = MetaData()

comment = Table(
	'comment',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('content', String(500), default="Content"),
	Column('user_id', Integer, ForeignKey(user.c.id, ondelete='CASCADE')),
	Column('video_id', Integer, ForeignKey(video.c.id, ondelete='CASCADE')),
)
