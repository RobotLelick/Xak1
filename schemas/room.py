from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название комнаты")
    description: Optional[str] = Field(None, max_length=500, description="Описание комнаты")


class RoomCreate(RoomBase):
    """Схема для создания комнаты"""
    pass


class Room(RoomBase):
    """Схема для ответа с данными комнаты"""
    id: int
    invite_code: str
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RoomJoin(BaseModel):
    """Схема для присоединения по коду"""
    invite_code: str = Field(..., min_length=5, max_length=20, description="Код приглашения")


class RoomInvite(BaseModel):
    """Схема для ответа с инвайт-кодом"""
    invite_code: str


class RoomMember(BaseModel):
    """Схема для участника комнаты"""
    id: int
    username: str
    email: str
    joined_at: datetime

    class Config:
        from_attributes = True


class RoomDetail(Room):
    """Детальная информация о комнате с участниками"""
    members: list[RoomMember] = []
    owner: Optional[RoomMember] = None