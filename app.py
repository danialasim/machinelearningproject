from flask import Flask, render_template, request, jsonify
import os 
import numpy as np
import pandas as pd
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline


app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    try:
        os.system("python main.py")
        return "<h1 style='text-align: center; color: green; font-family: Arial;'>✅ Training Successful!</h1><p style='text-align: center;'><a href='/' style='color: #667eea; text-decoration: none;'>← Back to Prediction</a></p>"
    except Exception as e:
        return f"<h1 style='text-align: center; color: red; font-family: Arial;'>❌ Training Failed!</h1><p style='text-align: center; color: #666;'>Error: {str(e)}</p><p style='text-align: center;'><a href='/' style='color: #667eea; text-decoration: none;'>← Back to Prediction</a></p>"


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            fixed_acidity = float(request.form['fixed_acidity'])
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])
            residual_sugar = float(request.form['residual_sugar'])
            chlorides = float(request.form['chlorides'])
            free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])

            # Validate input ranges (basic validation)
            validation_rules = {
                'fixed_acidity': (3.8, 15.9),
                'volatile_acidity': (0.08, 1.58),
                'citric_acid': (0.0, 1.66),
                'residual_sugar': (0.6, 65.8),
                'chlorides': (0.009, 0.611),
                'free_sulfur_dioxide': (1.0, 289.0),
                'total_sulfur_dioxide': (6.0, 440.0),
                'density': (0.98711, 1.03898),
                'pH': (2.72, 4.01),
                'sulphates': (0.22, 2.0),
                'alcohol': (8.0, 15.0)
            }

            # Check if values are within expected ranges
            inputs = {
                'fixed_acidity': fixed_acidity,
                'volatile_acidity': volatile_acidity,
                'citric_acid': citric_acid,
                'residual_sugar': residual_sugar,
                'chlorides': chlorides,
                'free_sulfur_dioxide': free_sulfur_dioxide,
                'total_sulfur_dioxide': total_sulfur_dioxide,
                'density': density,
                'pH': pH,
                'sulphates': sulphates,
                'alcohol': alcohol
            }

            for field, value in inputs.items():
                min_val, max_val = validation_rules[field]
                if not (min_val <= value <= max_val):
                    return render_template('index.html', error=f"⚠️ {field.replace('_', ' ').title()} should be between {min_val} and {max_val}")
         
            data = [fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, 
                   free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]
            data = np.array(data).reshape(1, 11)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)

            # Round the prediction to 2 decimal places for better display
            prediction_value = round(float(predict[0]), 2)

            return render_template('results.html', prediction=prediction_value)

        except ValueError as ve:
            return render_template('index.html', error="⚠️ Please enter valid numeric values for all fields")
        except Exception as e:
            print('The Exception message is: ', e)
            return render_template('index.html', error=f"⚠️ Prediction failed: {str(e)}")

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)