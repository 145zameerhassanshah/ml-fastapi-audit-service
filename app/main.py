from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.audit import fetch_recent_logs, log_request
from app.database import init_database
from app.model_service import MODEL_VERSION, load_model, predict
from app.schemas import PredictionInput, PredictionResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    load_model()
    yield

app = FastAPI(
    title="ML Prediction API with Audit Logging",
    description="Educational FastAPI service serving a trained classifier with SQLite audit logging.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health() -> dict:
    return {"status":"ok","timestamp_utc":datetime.now(timezone.utc).isoformat(),"model_version":MODEL_VERSION}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raw_body = (await request.body()).decode("utf-8", errors="replace")
    error_message = "; ".join(f"{'.'.join(str(x) for x in e['loc'] if x != 'body')}: {e['msg']}" for e in exc.errors())
    log_request(status="failed", request_payload=raw_body, error_message=error_message, model_version=MODEL_VERSION)
    return JSONResponse(status_code=400, content={"error":"Invalid prediction request","details":exc.errors()})

@app.post("/predict", response_model=PredictionResponse)
def make_prediction(payload: PredictionInput) -> dict:
    data = payload.model_dump()
    try:
        predicted_class, probability = predict(data)
        probability = round(probability, 6)
        log_request(status="success", request_payload=data, predicted_class=predicted_class, probability_class_1=probability, model_version=MODEL_VERSION)
        return {"predicted_class":predicted_class,"probability_class_1":probability,"model_version":MODEL_VERSION}
    except Exception as exc:
        log_request(status="failed", request_payload=data, error_message=str(exc), model_version=MODEL_VERSION)
        raise HTTPException(status_code=500, detail="Prediction failed. The request was logged for audit.") from exc

@app.get("/audit")
def audit_trail(limit: int = Query(default=20, ge=1, le=100)) -> list[dict]:
    return fetch_recent_logs(limit)
