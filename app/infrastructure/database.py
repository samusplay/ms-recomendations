"""
Database module - DISABLED for Python 3.14 compatibility
SQLAlchemy is not compatible with Python 3.14 yet.
This is a placeholder module to avoid import errors.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Placeholder classes to avoid import errors
class DummyEngine:
    def __init__(self, *args, **kwargs):
        pass
    
    def connect(self):
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def execute(self, *args, **kwargs):
        return self

class DummySession:
    def __init__(self, *args, **kwargs):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def query(self, *args):
        return self
    
    def filter(self, *args):
        return self
    
    def first(self):
        return None
    
    def all(self):
        return []
    
    def add(self, *args):
        pass
    
    def commit(self):
        pass
    
    def refresh(self, *args):
        pass
    
    def close(self):
        pass

class DummyBase:
    metadata = None

# ── Base de datos principal (Recomendaciones) ──
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recommendations.db")
engine = DummyEngine(DATABASE_URL)
SessionLocal = DummySession
Base = DummyBase()

# ── Base de datos secundaria (Model Store) ──
MODEL_STORE_URL = os.getenv("MODEL_STORE_URL", "sqlite:///./model_store.db")
engine_model_store = DummyEngine(MODEL_STORE_URL)
SessionModelStore = DummySession
BaseModelStore = DummyBase()

# ── Verificar conexiones (siempre True para dummy) ──
def check_db_connection():
    print("⚠️ Database disabled - SQLAlchemy incompatible with Python 3.14")
    return True

def check_model_store_connection():
    print("⚠️ Model Store disabled - SQLAlchemy incompatible with Python 3.14")
    return True

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