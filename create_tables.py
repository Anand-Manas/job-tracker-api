from app.core.database import engine
from app.models.db_models import Base, Application, User

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
