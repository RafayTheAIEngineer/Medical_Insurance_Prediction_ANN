from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal
import numpy as np
import joblib
from keras.models import load_model

# initialize API
app = FastAPI(
    title = 'Medical Insurance Cost Predictor API',
    description='Deep Learning model to predict medical insurance charges based on patient data',
    version='1.0'
)

# Load Scaler and model 
try:
    model = load_model('medical_insurance_model.keras')
    scaler = joblib.load('insurance_scaler.joblib')
    print('Model and Sacler loaded successfully')
except Exception as e:
    raise RuntimeError(f'Failed to load the Model and Scaler: {str(e)}')


# Pydantic Model (For data validation)
class PatientData(BaseModel):
    age: int = Field(
        default=30, 
        ge=18, 
        le=100, 
        examples=[20], 
        description='Age of patient must be between 18 and 100'
        )
    sex: Literal['male', 'female'] = Field(
        default='male', 
        examples=['male'], 
        description='Gender of patient [male, female]'
        )
    bmi: float = Field(
        default=25.0, 
        gt=10.0, 
        lt=60.0, 
        description='Body Mass Index (BMI). Normal range between 10 and 60',
        examples=[20.0]
        )
    children: int = Field(
        default=2, 
        ge=0, 
        le=10, 
        description='Number of children (between 0 and 10)',
        examples=[5]
        )
    smoker: Literal['yes', 'no'] = Field(
        default='no',
        description='Does the patient smoke? (Yes or No)',
        examples=['yes']
        )
    region: Literal['southwest', 'southeast', 'northwest', 'northeast'] = Field(
        default='northeast',
        description="US ka region ('southwest', 'southeast', 'northwest', 'northeast')"
        )


# prediction endpoint
@app.post('/predict')
def predict_charges(data:PatientData):
    try:
        # --- Data Extraction and Encoding ---
        sex_encoded = 1 if data.sex.lower() == 'male' else 0
        smoker_encoded = 1 if data.smoker.lower() == 'yes' else 0

        region_northwest = 1 if data.region.lower() == 'northwest' else 0
        region_southeast = 1 if data.region.lower() == 'southeast' else 0
        region_southwest = 1 if data.region.lower() == 'southwest' else 0

        # --- Feature Engineering ---
        smoker_bmi_interaction = smoker_encoded * data.bmi
        high_risk_smoker = 1 if (smoker_encoded == 1 and data.bmi > 30) else 0

        # Array Assembly
        # order must match with training data exactly
        input_featues = np.array([[
            data.age, sex_encoded, data.bmi, data.children, smoker_encoded,
            region_northwest, region_southeast, region_southwest,
            smoker_bmi_interaction, high_risk_smoker
        ]])

        # --- scaling --- 
        scaled_features = scaler.transform(input_featues)

        # --- Model Prediction ---
        log_prediction = model.predict(scaled_features)[0][0]

        # --- inverse log trasform ---
        final_charge = np.expm1(log_prediction)

        # return json response
        return JSONResponse(
            status_code=200,
            content={
                'patient_profile' :{
                    'age' : data.age,
                    'bmi' : data.bmi,
                    'smoker' : data.smoker
                },
                'predicted_insurance_charges' : round(float(final_charge), 2)
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Root endpoint check karne ke liye API zinda hai ya nahi
@app.get("/ping")
def read_root():
    return {"message": "Ok"}