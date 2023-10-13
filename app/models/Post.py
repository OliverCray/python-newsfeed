from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property

class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  post_url = Column(String(100), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  user = relationship('User')
  comments = relationship('Comment', cascade='all,delete')
  votes = relationship('Vote', cascade='all,delete')

  @hybrid_property
  def vote_count(self):
      # Calculate the vote count using Python
      return sum(vote.value for vote in self.votes)

  @vote_count.expression
  def vote_count(cls):
      # Calculate the vote count using SQL
      return (
          select([func.sum(Vote.value)])
          .where(Vote.post_id == cls.id)
          .label("vote_count")
      )
