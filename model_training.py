# model_training.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load the data
df = pd.read_excel('Cleaned Car.xlsx')

# Data preprocessing
# Convert categorical variables to numerical using Label Encoding
le_company = LabelEncoder()
le_model = LabelEncoder()
le_fuel_type = LabelEncoder()

df['company_encoded'] = le_company.fit_transform(df['company'])
df['name_encoded'] = le_model.fit_transform(df['name'])
df['fuel_type_encoded'] = le_fuel_type.fit_transform(df['fuel_type'])

# Save the encoders for later use
with open('company_encoder.pkl', 'wb') as f:
    pickle.dump(le_company, f)
with open('model_encoder.pkl', 'wb') as f:
    pickle.dump(le_model, f)
with open('fuel_type_encoder.pkl', 'wb') as f:
    pickle.dump(le_fuel_type, f)

# Features and target
X = df[['company_encoded', 'name_encoded', 'year', 'kms_driven', 'fuel_type_encoded']]
y = df['Price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
with open('LinearRegressionModel.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save the unique values of categorical variables for the frontend
companies = sorted(df['company'].unique())
car_models = sorted(df['name'].unique())
years = sorted(df['year'].unique(), reverse=True)
fuel_types = df['fuel_type'].unique()

# Save these lists for use in the frontend
with open('companies.pkl', 'wb') as f:
    pickle.dump(companies, f)
with open('car_models.pkl', 'wb') as f:
    pickle.dump(car_models, f)
with open('years.pkl', 'wb') as f:
    pickle.dump(years, f)
with open('fuel_types.pkl', 'wb') as f:
    pickle.dump(fuel_types, f)

# Create and save company-to-car-models mapping
company_car_mapping = {}
for company in companies:
    company_car_mapping[company] = df[df['company'] == company]['name'].unique().tolist()

with open('company_car_mapping.pkl', 'wb') as f:
    pickle.dump(company_car_mapping, f)

print("Model and data files saved successfully!")
print(f"Created mapping for {len(companies)} companies with their respective car models.")
