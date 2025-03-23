
# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Define paths to model and encoders
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, 'LinearRegressionModel.pkl')
company_encoder_path = os.path.join(base_dir, 'company_encoder.pkl')
model_encoder_path = os.path.join(base_dir, 'model_encoder.pkl')
fuel_type_encoder_path = os.path.join(base_dir, 'fuel_type_encoder.pkl')
companies_path = os.path.join(base_dir, 'companies.pkl')
car_models_path = os.path.join(base_dir, 'car_models.pkl')
years_path = os.path.join(base_dir, 'years.pkl')
fuel_types_path = os.path.join(base_dir, 'fuel_types.pkl')
company_car_mapping_path = os.path.join(base_dir, 'company_car_mapping.pkl')

# Load model and encoders
model = pickle.load(open(model_path, 'rb'))
company_encoder = pickle.load(open(company_encoder_path, 'rb'))
model_encoder = pickle.load(open(model_encoder_path, 'rb'))
fuel_type_encoder = pickle.load(open(fuel_type_encoder_path, 'rb'))

# Load dropdown options
companies = pickle.load(open(companies_path, 'rb'))
car_models = pickle.load(open(car_models_path, 'rb'))
years = pickle.load(open(years_path, 'rb'))
fuel_types = pickle.load(open(fuel_types_path, 'rb'))
company_car_mapping = pickle.load(open(company_car_mapping_path, 'rb'))

@app.route('/')
def home():
    return render_template('index.html', 
                          companies=companies, 
                          car_models=car_models,  # All car models (will be filtered by JavaScript)
                          years=years, 
                          fuel_types=fuel_types,
                          company_car_mapping=company_car_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        company = request.form.get('company')
        car_model = request.form.get('car_model')
        year = int(request.form.get('year'))
        fuel_type = request.form.get('fuel_type')
        kms_driven = int(request.form.get('kms_driven'))
        
        # Encode categorical variables
        company_encoded = company_encoder.transform([company])[0]
        model_encoded = model_encoder.transform([car_model])[0]
        fuel_type_encoded = fuel_type_encoder.transform([fuel_type])[0]
        
        # Create input array for prediction
        input_data = np.array([[company_encoded, model_encoded, year, kms_driven, fuel_type_encoded]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        # Format prediction as currency
        formatted_prediction = f"₹{prediction:,.2f}"
        
        return render_template('index.html', 
                              prediction_text=formatted_prediction, 
                              companies=companies, 
                              car_models=car_models,
                              years=years, 
                              fuel_types=fuel_types,
                              selected_company=company, 
                              selected_model=car_model,
                              selected_year=year, 
                              selected_fuel=fuel_type,
                              kms_driven=kms_driven,
                              company_car_mapping=company_car_mapping)
    except Exception as e:
        return render_template('index.html', 
                              error=str(e),
                              companies=companies, 
                              car_models=car_models,
                              years=years, 
                              fuel_types=fuel_types,
                              company_car_mapping=company_car_mapping)

if __name__ == '__main__':
    app.run(debug=True)
