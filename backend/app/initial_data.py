import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(user)
        db.commit()
        logger.info("Created initial admin user")

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")

if __name__ == "__main__":
    main() 