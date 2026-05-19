# app/routers/api.py
from fastapi import APIRouter

# Importamos la variable 'router' que definiste en recommendation_router.py
from app.routers.recommendation_router import router as recommendation_router

api_router = APIRouter()

api_router.include_router(
    recommendation_router, 
    tags=["Recomendaciones Territoriales"]
)