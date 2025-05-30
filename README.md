# Flask URL Prediction API

This is a Flask-based API for URL prediction, including CRUD operations.

## Features

- Predict whether a URL is malicious or benign
- CRUD endpoints:
  - Create new prediction
  - Read predictions
  - Update predictions
  - Delete predictions

## Requirements

- Python 3.11+
- pip
- Docker (optional for deployment)

## Installation

Clone the repository:
git clone https://github.com/...
cd flask-api

## Virtual environment and install dependenceies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

## Run app locally
python app.py

## API Endpoints
1. GET /                ---> Health check route.
2. POST /predictions    ---> Create a new URL prediction.
{
  "url": "https://example.com"
}
3. GET /predictions         ---> Retrieve all predictions.
4. GET /predictions/<id>    ---> Retrieve prediction by ID.
5. PUT /predictions/<id>    ---> Update a prediction by ID.
6. DELETE /predictions/<id> ---> Delete a prediction by ID.
7. GET /predictions/url?url=<url> ---> Retrieve prediction by URL.
