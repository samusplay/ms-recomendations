import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# ── Base de datos principal (Recomendaciones) ──
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Base de datos secundaria (Model Store) ──
MODEL_STORE_URL = os.getenv("MODEL_STORE_URL")
engine_model_store = create_engine(MODEL_STORE_URL)
SessionModelStore = sessionmaker(autocommit=False, autoflush=False, bind=engine_model_store)
BaseModelStore = declarative_base()


# ── Verificar conexiones ──
def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"\033[91m❌ Error crítico conectando a db-recommendations: {e}")
        return False

def check_model_store_connection():
    try:
        with engine_model_store.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"\033[91m❌ Error crítico conectando a db-model-store: {e}")
        return False


# ── Sesiones ──
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_model_store_db():
    db = SessionModelStore()
    try:
        yield db
    finally:
        db.close()