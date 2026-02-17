"""
FastAPI Inference Service
--------------------------
Endpoints:
  GET  /health   — Liveness check
  POST /predict  — Schema-validated prediction
  GET  /metrics  — Prometheus format metrics
  GET  /dropdown-values — Valid dropdown values for frontend

Prometheus instrumentation:
  - request_count: total requests by endpoint and status
  - prediction_count: total predictions served
  - request_latency: histogram of request duration
  - prediction_errors: total prediction errors
"""

import os
import sys
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.schemas import (
    PredictionRequest,
    PredictionResponse,
    HealthResponse,
    DropdownValues,
)
from inference.model_loader import ModelLoader

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("inference")

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter(
    "api_request_total",
    "Total API requests",
    ["method", "endpoint", "status"],
)
PREDICTION_COUNT = Counter(
    "api_prediction_total",
    "Total predictions served",
)
REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "Request duration in seconds",
    ["endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)
PREDICTION_ERRORS = Counter(
    "api_prediction_errors_total",
    "Total prediction errors",
)
MODEL_INFO = Gauge(
    "model_info",
    "Model version information",
    ["version"],
)

# --- Model ---
model_loader = ModelLoader()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup."""
    model_path = os.environ.get("MODEL_PATH", "models/model.joblib")
    preprocessor_path = os.environ.get(
        "PREPROCESSOR_PATH", "data/processed/preprocessor.joblib"
    )

    try:
        model_loader.load(model_path, preprocessor_path)
        MODEL_INFO.labels(version=model_loader.version).set(1)
        logger.info(f"Model loaded successfully: {model_loader.version}")
    except Exception as e:
        logger.critical(f"CRITICAL: Failed to load model: {e}")
        logger.critical("Service cannot start without model. Exiting...")
        # STRICT: Fail Fast. 
        # Do not start in a zombie state. Force orchestrator to restart.
        raise e
    
    yield


# --- App ---
# --- Security Headers & Middleware ---
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    title="Clinical Treatment Outcome Prediction API",
    description=(
        "This system predicts patient treatment outcome scores to support "
        "clinical research, quality analysis, and exploratory analytics. "
        "It does not provide diagnostic or treatment recommendations."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Enforce allowed hosts
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "inference-api"]
)

# --- CORS ---
# SEC-01: Inject Allowed Origins via Env Var
# ARC-01: With Nginx Reverse Proxy, CORS is largely handled by Same-Origin,
# but we keep strict allow-list for direct API access patterns if needed.
_origins_str = os.environ.get("ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
ALLOWED_ORIGINS = [origin.strip() for origin in _origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# --- Security Headers ---
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# --- Middleware for request logging ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.4f}s"
    )

    return response


# --- Endpoints ---
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check(response: Response):
    """Liveness and readiness check."""
    if not model_loader.is_loaded:
        response.status_code = 503
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_version="unknown",
        )

    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_version=model_loader.version,
    )



@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Predict treatment outcome improvement score.

    Input is schema-validated against the CSV dataset contract.
    Returns predicted Improvement_Score on a 0-10 scale.
    """
    if not model_loader.is_loaded:
        PREDICTION_ERRORS.inc()
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Prepare input (exclude Patient_ID — not a predictive feature)
        input_data = {
            "Age": request.Age,
            "Gender": request.Gender,
            "Condition": request.Condition,
            "Drug_Name": request.Drug_Name,
            "Dosage_mg": request.Dosage_mg,
            "Treatment_Duration_days": request.Treatment_Duration_days,
            "Side_Effects": request.Side_Effects,
        }

        prediction = model_loader.predict(input_data)
        PREDICTION_COUNT.inc()

        return PredictionResponse(
            Patient_ID=request.Patient_ID,
            Improvement_Score=prediction,
            model_version=model_loader.version,
        )

    except Exception as e:
        PREDICTION_ERRORS.inc()
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed due to an internal error.")


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return PlainTextResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/dropdown-values", response_model=DropdownValues, tags=["Frontend"])
async def dropdown_values():
    """Return valid dropdown values for the frontend form."""
    return DropdownValues()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
