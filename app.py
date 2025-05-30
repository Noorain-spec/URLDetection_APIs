from flask import Flask, request, jsonify
import joblib
import os
import re
from flask_sqlalchemy import SQLAlchemy
from feature_extraction import extract_features

app = Flask(__name__)

#loading model
model= joblib.load('ml_model/url_model.joblib')
model_features = joblib.load('ml_model/model_features.joblib')

#assign db deatils
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB columns
class URLPrediction(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    url = db.Column(db.String(1000), nullable= False)
    prediction = db.Column(db.String(500), nullable= False)

# Create DB table
with app.app_context():
    db.create_all()

#predict url
@app.route('/predict', methods=['POST'])
def predict_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': "No url provided"}), 400

    #send url input for feature extraction
    features = extract_features(url, model_features)
    prediction = model.predict(features)[0]
    labels = {0: "benign", 1: "defacement", 2: "phishing", 3: "malware"}
    #print(f"Prediction for URL '{url}': {labels[prediction]}")

    #check if db have same url
    url_db = URLPrediction.query.filter_by(url=url)
    #if url_db:
    #    if url_db.prediction != labels[prediction]:
    #        return jsonify ({'error': f'update the {url} value with correct prediction found mismatched predictions'})
    
    # save values to DB
    url_pred = URLPrediction(url=url, prediction=labels[prediction])
    db.session.add(url_pred)
    db.session.commit()

    return jsonify({'url': url, 'prediction': labels[prediction]})

# get all predictions
@app.route('/predictions', methods = ['GET'])
def get_all_predictions():
    preds = URLPrediction.query.all()
    return jsonify([
        {'id':  p.id, 'url': p.url, 'prediction': p.prediction}
        for p in preds
    ])

#get prediction by ID
@app.route('/predictions/<int:id>', methods=['GET'])
def get_prediction_by_ID(id):
    p = URLPrediction.query.get(id)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'id': p.id, 'url': p.url, 'prediction': p.prediction})

#get prediction by url
@app.route('/predictions/url', methods= ['GET'])
def get_prediction():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No url found in request'}), 400
    
    p = URLPrediction.query.filter_by(url=url).first()
    if not p:
        return jsonify({'error': 'URL Not found'}), 404
    return jsonify({'id': p.id, 'url': p.url, 'prediction': p.prediction})

#update prediction by id
@app.route('/predictions/<int:id>', methods=['PUT'])
def update_prediction(id):
    p = URLPrediction.query.get(id)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    
    data = request.get_json()
    p.url = data.get('url', p.url)
    p.prediction = data.get('prediction', p.prediction)
    db.session.commit()
    return jsonify({'message': 'Updated', 'id': p.id})

#delete prediction by id
@app.route('/predictions/<int:id>', methods=['DELETE'])
def delete_prediction(id):
    p= URLPrediction.query.get(id)
    if not p:
        return jsonify({'error': 'Wrong ID/ID not found'}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Deleted sucessfully', 'id': id})

#HealthCheck
@app.route('/')
def index():
    return jsonify({'mesage': 'URL prediction API running!'})

if __name__ == '__main__':
    app.run(debug = True)

