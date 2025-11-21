"""
bot/database/database.py
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from bot.config import Config
from bot.database.models import Base

logger = logging.getLogger(__name__)


class Database:
    """Database manager"""
    
    def __init__(self):
        self.engine = create_engine(
            Config.DATABASE_URL,
            echo=False,
            pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self._create_tables()
    
    def _create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created")
    
    @contextmanager
    def get_session(self) -> Session:
        """Get database session"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    def get_or_create_user(self, telegram_id: int, username: str = None, first_name: str = None):
        """Get or create user"""
        from bot.database.models import User
        
        with self.get_session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name
                )
                session.add(user)
                session.commit()
                logger.info(f"Created new user: {telegram_id}")
            else:
                # Update last active
                user.last_active = datetime.utcnow()
                if username:
                    user.username = username
                if first_name:
                    user.first_name = first_name
                session.commit()
            
            return user
    
    def create_generated_bot(self, user_telegram_id: int, bot_data: dict):
        """Create generated bot record"""
        from bot.database.models import User, GeneratedBot
        
        with self.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
            
            if not user:
                raise ValueError(f"User {user_telegram_id} not found")
            
            bot = GeneratedBot(
                user_id=user.id,
                bot_id=bot_data['bot_id'],
                name=bot_data['name'],
                description=bot_data.get('description', ''),
                prompt=bot_data.get('prompt', ''),
                language=bot_data['language'],
                framework=bot_data['framework'],
                directory_path=bot_data['directory_path'],
                archive_path=bot_data.get('archive_path'),
                file_count=len(bot_data.get('files', {})),
                env_vars_count=len(bot_data.get('env_vars', []))
            )
            
            session.add(bot)
            
            # Increment user generation count
            user.generation_count += 1
            
            session.commit()
            logger.info(f"Created bot record: {bot.bot_id}")
            
            return bot
    
    def get_user_bots(self, telegram_id: int, limit: int = 10):
        """Get user's generated bots"""
        from bot.database.models import User, GeneratedBot
        
        with self.get_session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            
            if not user:
                return []
            
            bots = session.query(GeneratedBot)\
                .filter_by(user_id=user.id, is_deleted=False)\
                .order_by(GeneratedBot.created_at.desc())\
                .limit(limit)\
                .all()
            
            return bots
    
    def mark_bot_deployed(self, bot_id: str):
        """Mark bot as deployed"""
        from bot.database.models import GeneratedBot
        
        with self.get_session() as session:
            bot = session.query(GeneratedBot).filter_by(bot_id=bot_id).first()
            
            if bot:
                bot.is_deployed = True
                bot.deployed_at = datetime.utcnow()
                session.commit()
                logger.info(f"Marked bot {bot_id} as deployed")
    
    def create_repo_scan(self, user_telegram_id: int, scan_data: dict):
        """Create repo scan record"""
        from bot.database.models import User, RepoScan
        
        with self.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
            
            if not user:
                raise ValueError(f"User {user_telegram_id} not found")
            
            scan = RepoScan(
                user_id=user.id,
                repo_url=scan_data['repo_url'],
                language=scan_data.get('language'),
                framework=scan_data.get('framework'),
                env_vars_found=len(scan_data.get('env_vars', [])),
                dependencies_found=len(scan_data.get('dependencies', []))
            )
            
            session.add(scan)
            session.commit()
            logger.info(f"Created repo scan record: {scan.repo_url}")
            
            return scan


# Initialize database
db = Database()
