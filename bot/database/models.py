"""
YAGAMI UNIVERZE - Database Models
bot/database/models.py
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_banned = Column(Boolean, default=False)
    generation_count = Column(Integer, default=0)

    # Relationships
    bots = relationship("GeneratedBot", back_populates="user")

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class GeneratedBot(Base):
    """Generated bot model"""
    __tablename__ = 'generated_bots'

    id = Column(Integer, primary_key=True)
    bot_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    prompt = Column(Text, nullable=False)

    language = Column(String(50), nullable=False)
    framework = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    deployed_at = Column(DateTime, nullable=True)

    is_deployed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    directory_path = Column(String(500), nullable=False)
    archive_path = Column(String(500), nullable=True)

    file_count = Column(Integer, default=0)
    env_vars_count = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="bots")

    def __repr__(self):
        return f"<GeneratedBot(bot_id={self.bot_id}, name={self.name})>"


class RepoScan(Base):
    """Repository scan model"""
    __tablename__ = 'repo_scans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    repo_url = Column(String(500), nullable=False)
    language = Column(String(50), nullable=True)
    framework = Column(String(50), nullable=True)

    env_vars_found = Column(Integer, default=0)
    dependencies_found = Column(Integer, default=0)

    scanned_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RepoScan(repo_url={self.repo_url})>"
