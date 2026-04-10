# Genderize Classifier API
A FastAPI service that classifies names by gender using the Genderize API.
### Genderize_API = 'https://api.genderize.io/'

## Endpoint
### `GET /api/classify?name={name}`

**Error Responses**
#### 400 : Missing or empty `name` parameter 
#### 422 :`name` is not a valid string 
#### 502 : Upstream (Genderize) API failure 
#### 500 : Internal server error 

### All errors return:
```json
{ "status": "error", "message": "<description>" }
```
## Run Locally
#### Clone the repo
git clone https://github.com/ajibua/genderize-api/
cd genderize-api-py

#### Creating a virtual environment
python -m venv venv
venv\Scripts\activate

#### Installing dependencies
pip install -r requirements.txt

#### Starting  the server with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

#### To run test in terminal 
curl "http://localhost:8000/api/classify?name=<any-demo-name>"

## Stack
- **Language:** Python 3.13+
- **Framework:** FastAPI
- **HTTP Client:** httpx (async)
- **Server:** Uvicorn
