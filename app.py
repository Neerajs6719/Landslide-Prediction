from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('random_forest_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            temp = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            precipitation = float(request.form['precipitation'])
            soil_moisture = float(request.form['soil_moisture'])
            elevation = float(request.form['elevation'])
            
            # Create DataFrame for prediction
            data = [[temp, humidity, precipitation, soil_moisture, elevation]]
            columns = ['Temperature (°C)', 'Humidity (%)', 'Precipitation (mm)', 
                      'Soil Moisture (%)', 'Elevation (m)']
            df = pd.DataFrame(data, columns=columns)
            
            # Make prediction
            # Map numeric prediction to string label
            class_labels = {
                            0: 'Low',
                            1: 'Medium',  
                            2: 'High'
}

            raw_prediction = model.predict(df)[0]
            prediction = class_labels[int(raw_prediction)]
            probability = np.max(model.predict_proba(df)) * 100

            
            # Risk level mapping
            risk_levels = {
                'Low': 'success',
                'Moderate': 'warning',
                'High': 'danger',
                'Very High': 'danger'
            }
            
            return render_template('result.html', 
                                prediction=prediction,
                                probability=f"{probability:.2f}",
                                risk_class=risk_levels[prediction],
                                temp=temp,
                                humidity=humidity,
                                precipitation=precipitation,
                                soil_moisture=soil_moisture,
                                elevation=elevation)
        
        except Exception as e:
            return render_template('predict.html', error=str(e))
    
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
