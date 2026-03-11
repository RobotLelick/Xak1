from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
import secrets

Model = declarative_base()

room_members = Table(
    'room_members',
    Model.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('joined_at', DateTime, server_default=func.now())
)


class Room(Model):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    invite_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id])
    members = relationship("User", secondary=room_members, back_populates="rooms")

    @staticmethod
    def generate_invite_code():
        return secrets.token_urlsafe(8)