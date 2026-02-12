from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Boolean, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.database.core import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, default="User")
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    custom_api_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    current_model: Mapped[str] = mapped_column(String, default="google/gemini-2.0-flash-lite-preview-02-05:free")
    current_role: Mapped[str] = mapped_column(String, default="assistant")
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    is_unlimited: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # State management
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    state_data: Mapped[Optional[str]] = mapped_column(String, nullable=True) # JSON string


    error_logs: Mapped[list["ErrorLog"]] = relationship(back_populates="user")

class ErrorLog(Base):
    __tablename__ = "error_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    error_text: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    traceback: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="error_logs")
