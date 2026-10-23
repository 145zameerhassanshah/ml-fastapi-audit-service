# ML Model Served via FastAPI with Automatic Logging

A production-style educational milestone that serves a trained scikit-learn classification model through a FastAPI `/predict` endpoint and automatically records successful and failed requests in SQLite.

> **Important:** The model is trained on synthetic health-like data for software-engineering practice only. It is not a clinical model and must not be used for diagnosis, treatment, or real patient decision-making.

## Requirements Covered
- `/predict` endpoint with validated input
- predicted class and class-1 probability
- trained model serialized with joblib
- automatic SQLite logging of success and failure
- audit trail endpoint and CLI demonstration
- README setup and example requests
- documented limitations
- automated tests

## Architecture
```text
Client -> POST /predict -> Pydantic validation -> ML model -> prediction/probability -> SQLite audit log -> JSON
                         \-> invalid request -> failed SQLite audit log -> HTTP 400
```

## Inputs
`age` 18-100, `systolic` 70-250, `diastolic` 40-150, `glucose` >0 to 500, `bmi` >10 to 70. These are software validation ranges, not clinical thresholds.

## Setup
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/train_model.py
python -m uvicorn app.main:app --reload
```
Swagger: `http://127.0.0.1:8000/docs`

## Example `/predict`
```json
{"age":52,"systolic":138,"diastolic":86,"glucose":126.5,"bmi":29.4}
```
Example response:
```json
{"predicted_class":1,"probability_class_1":0.734281,"model_version":"1.0.0"}
```
The probability is a model output for synthetic class 1, not a medical risk probability.

## Audit Trail
Successful and failed prediction requests are stored in `audit.db` with UTC timestamp, payload, status, class, probability, error, and model version.

View via API:
`GET /audit?limit=10`

Or CLI:
```powershell
python scripts/show_audit.py
```

## Invalid Request Example
```json
{"age":"wrong-type","systolic":138,"diastolic":86,"glucose":126.5,"bmi":29.4}
```
Expected: HTTP 400, and a failed audit row is written.

## Tests
```powershell
pytest
```
Covers successful inference, probability range, success logging, invalid types, out-of-range values, missing fields, failure logging, health, and audit limit.

## Limitations
1. Synthetic training data only; not clinically validated.
2. SQLite is suitable for local/small services, not distributed high-volume production.
3. Authentication/authorization are out of scope.
4. Real sensitive payload logging would require minimization, encryption, access controls, and retention policies.
5. No drift monitoring, model registry, rate limiting, or production observability.

## Example curl
```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{\"age\":52,\"systolic\":138,\"diastolic\":86,\"glucose\":126.5,\"bmi\":29.4}"
```
