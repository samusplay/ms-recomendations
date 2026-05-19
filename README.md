# 🎯 MS-RECOMMENDATIONS

## Microservicio de Recomendaciones Territoriales

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![SOLID](https://img.shields.io/badge/SOLID-100%25-red.svg)](https://en.wikipedia.org/wiki/SOLID)
[![Hexagonal](https://img.shields.io/badge/Architecture-Hexagonal-purple.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture)

---

## 📋 Descripción

Microservicio que **genera recomendaciones inteligentes** para inversión territorial, combinando:

- **Score territorial** (desde `ms-analytics-scoring`)
- **Predicción ML** (desde `ms-machine-learning`)

Transforma datos técnicos en **recomendaciones explicadas** para la toma de decisiones de negocio.

---

## 🏗️ Arquitectura

### Hexagonal (Ports & Adapters) + SOLID

---

## ✅ Principios SOLID

| Principio | Aplicación |
|-----------|------------|
| **S**ingle Responsibility | Cada clase tiene una única responsabilidad |
| **O**pen/Closed | Abierto para extensión, cerrado para modificación |
| **L**iskov Substitution | Adaptadores pueden sustituir a los puertos |
| **I**nterface Segregation | Interfaces pequeñas y específicas |
| **D**ependency Inversion | Depender de abstracciones, no de implementaciones |

---

## 📦 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/recommendations/health` | Health check |
| `GET` | `/api/v1/recommendations/` | Información del servicio |
| `GET` | `/api/v1/recommendations/{zone_code}` | Recomendación por zona |

---

## 📊 Ejemplo de Respuesta

### ✅ Éxito (200 OK)

```json
{
  "success": true,
  "data": {
    "zone_code": "11001",
    "zone_name": "Bogotá",
    "score": {
      "value": 87.5,
      "level": "alta oportunidad"
    },
    "prediction": {
      "potential_value": 85.5,
      "confidence_score": 0.85,
      "business_label": "Alto Potencial",
      "color_code": "#22c55e"
    },
    "strengths": [
      "✅ Puntuación general muy alta, zona prioritaria",
      "📈 Alto potencial de crecimiento proyectado",
      "🎯 Alta consistencia entre evaluación actual y proyección"
    ],
    "risks": [
      "🌟 Oportunidad con riesgo controlado"
    ],
    "opportunities": [
      "💼 Ideal para expansión de negocio existente",
      "🚀 Potencial para negocio ancla en la zona",
      "⭐ Zona candidata para inversión prioritaria"
    ],
    "final_recommendation": "INVERTIR PRIORITARIAMENTE - Excelente oportunidad",
    "summary": "Bogotá presenta oportunidad excepcional de inversión"
  },
  "error": null,
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}


❌ Error (422 Unprocessable Entity)
json
{
  "success": false,
  "error": {
    "code": "INVALID_ZONE_CODE_FORMAT",
    "message": "Formato inválido: '123'. Debe tener 5 u 11 dígitos."
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
🚀 Instalación y Ejecución
Requisitos Previos
Python 3.11 o superior

pip

Instalación
bash
# Clonar repositorio
git clone https://github.com/samusplay/ms-recomendations.git
cd ms-recomendations

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
Ejecución
bash
python run.py
Verificar que funciona
bash
curl http://localhost:8007/api/v1/recommendations/health
🔧 Variables de Entorno (.env)
env
# URLs de servicios
ML_SERVICE_URL=http://localhost:8000
SCORING_SERVICE_URL=http://localhost:8001

# Configuración del servidor
PORT=8007
HOST=127.0.0.1
RELOAD=True
🐳 Docker
Construir imagen
bash
docker build -t ms-recommendations .
Ejecutar contenedor
bash
docker run -p 8007:8007 ms-recommendations
🧪 Pruebas
Pruebas manuales
bash
# Health check
curl http://localhost:8007/api/v1/recommendations/health

# Recomendación Bogotá
curl http://localhost:8007/api/v1/recommendations/11001

# Error - formato inválido
curl http://localhost:8007/api/v1/recommendations/123
Documentación Swagger
Abrir en navegador: http://localhost:8007/docs

📁 Estructura del Proyecto
text
ms-recommendations/
├── app/
│   ├── main.py                          # Lifespan, configuración
│   ├── routers/
│   │   └── api.py                       # Controladores HTTP
│   ├── application/
│   │   ├── ports/
│   │   │   ├── score_port.py            # Puerto para scoring
│   │   │   └── ml_port.py               # Puerto para ML
│   │   └── use_cases/
│   │       └── get_recommendation_use_case.py
│   ├── domain/
│   │   ├── entities/
│   │   │   └── recommendation.py        # Entidades
│   │   └── services/
│   │       └── recommendation_engine.py # Lógica de negocio
│   └── infrastructure/
│       ├── adapters/
│       │   ├── score_rest_adapter.py    # Cliente HTTP scoring
│       │   └── ml_rest_adapter.py       # Cliente HTTP ML
│       └── database.py                  # Placeholder BD
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── run.py
🔌 Integración con otros Microservicios
Microservicio	Puerto	Endpoint
ms-machine-learning	8000	/api/v1/predictions/{zone_code}
ms-analytics-scoring	8001	/api/v1/score/{zone_code}
📊 Códigos de Estado
Código	Significado
200	OK - Recomendación generada
422	Formato de zone_code inválido
404	Zona no encontrada
503	Servicio dependiente no disponible
🎯 HU-22 Cumplimiento
Criterio	Estado
Endpoint GET /recommendations/{zone_code}	✅
Validación formato zone_code	✅
Respuesta estandarizada	✅
Errores sin stack trace	✅
Health check	✅
Consumo de ms-ml (puerto 8000)	✅
Consumo de ms-scoring (puerto 8001)	✅
Recomendaciones explicadas	✅
Principios SOLID	✅
Arquitectura hexagonal	✅

