from app.models import User
from app.database import SessionLocal, Base, engine
from passlib.context import CryptContext

# Crée les tables si besoin
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()
hashed_password = pwd_context.hash("admin")

if not db.query(User).filter_by(username="admin").first():
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hashed_password,
        is_active=True,
        role="admin"
    )
    db.add(admin)
    db.commit()
    print("Admin user created!")
else:
    print("Admin user already exists.")
db.close() 