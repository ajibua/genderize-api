# Genderize Classifier API

A FastAPI service that classifies names by gender using the [Genderize.io](https://genderize.io) API.

---

## Endpoint

### `GET /api/classify?name={name}`

**Success Response (200)**
```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-10T12:00:00Z"
  }
}
```

**Error Responses**

| Status | Reason |
|--------|--------|
| 400 | Missing or empty `name` parameter |
| 422 | `name` is not a valid string |
| 502 | Upstream (Genderize) API failure |
| 500 | Internal server error |

All errors return:
```json
{ "status": "error", "message": "<description>" }
```

---

## Run Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd genderize-api-py

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# 5. Test it
curl "http://localhost:8000/api/classify?name=john"
```

---

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Railway auto-detects Python. Set the start command to:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Done — Railway gives you a public URL.

## Deploy to Vercel

Add a `vercel.json` in the project root:
```json
{
  "builds": [{ "src": "main.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "main.py" }]
}
```
Then `vercel deploy`.

---

## Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **HTTP Client:** httpx (async)
- **Server:** Uvicorn