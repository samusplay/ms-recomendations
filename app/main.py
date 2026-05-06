from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database import (
    Base,
    BaseModelStore,
    check_db_connection,
    check_model_store_connection,
    engine,
    engine_model_store,
)
from app.routers.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\033[94m⚙️  Configurando servicios de Recomendaciones..\033[0m")
    
    # 1. Creamos tablas de Recomendaciones
    try:
        Base.metadata.create_all(bind=engine)
        print("\033[92m✅ Tablas de Recomendaciones sincronizadas\033[0m")
    except Exception as e:
        print(f"\033[91m🚨 Error creando tablas en db-recommendations: {e}\033[0m")

    # 2. Creamos tablas de Model Store
    try:
        BaseModelStore.metadata.create_all(bind=engine_model_store)
        print("\033[92m✅ Tablas de Model Store sincronizadas\033[0m")
    except Exception as e:
        print(f"\033[91m🚨 Error creando tablas en db-model-store: {e}\033[0m")

    # 3. Verificamos conexiones
    if check_db_connection():
        print("\033[92m✅ PERSISTENCIA: Conectado a db_recommendations\033[0m")
    else:
        print("\033[91m🚨 PERSISTENCIA: Fallo al conectar a db_recommendations\033[0m")

    if check_model_store_connection():
        print("\033[92m✅ PERSISTENCIA: Conectado a db_model_store\033[0m")
    else:
        print("\033[91m🚨 PERSISTENCIA: Fallo al conectar a db_model_store\033[0m")

    yield
    print("\033[93m\nFinalizando procesos de Recomendaciones...\033[0m")


app = FastAPI(
    title="API Recomendaciones",
    description="API para gestionar recomendaciones territoriales inteligentes",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1/recommendations")


@app.get("/api/v1/recommendations/health", tags=["Recomendaciones"])
def health():
    return {"status": "ok", "service": "ms-Recommendations"}