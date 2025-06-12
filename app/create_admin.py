from app.models import User
from app.database import SessionLocal, Base, engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()
hashed_password = pwd_context.hash("admin")  # mot de passe = admin

# Vérifie si l'utilisateur existe déjà
if not db.query(User).filter_by(username="admin").first():
    admin = User(username="admin", email="admin@example.com", hashed_password=hashed_password, is_active=True, role="admin")
    db.add(admin)
    db.commit()
    print("Admin user created!")
else:
    print("Admin user already exists.")
db.close()

# Ceci va créer toutes les tables définies dans tes modèles si elles n'existent pas
Base.metadata.create_all(bind=engine) 