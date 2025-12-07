import enum
import datetime
import secrets
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(str, enum.Enum):
    PLAYER = "player"
    HOST = "host"


def generate_join_code(length=15):
    return secrets.token_urlsafe(length)[:length]


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    join_code = Column(
        String(20), unique=True, nullable=False, index=True, default=generate_join_code
    )
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    users = relationship(
        "RoomUser", back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}', join_code='{self.join_code}')>"


class RoomUser(Base):
    __tablename__ = "room_users"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    username = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.PLAYER)
    joined_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    room = relationship("Room", back_populates="users")

    __table_args__ = (
        sqlalchemy.UniqueConstraint("room_id", "username", name="uq_room_username"),
    )

    def __repr__(self):
        return f"<RoomUser(id={self.id}, username='{self.username}', role='{self.role.value}')>"
