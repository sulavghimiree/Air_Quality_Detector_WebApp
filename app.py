from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    print(features)
    final_features = [np.array(features)]

    prediction = model.predict(final_features)
    if prediction[0] == 0:
        output = 'Good'
    elif prediction[0] == 1:
        output = 'Hazardious'
    elif prediction[0] == 2:
        output = 'Moderate'
    else:
        output = 'Poor'
    
    return render_template('result.html', prediction_text='Air Quality is {}'.format(output))

@app.route('/predict_general', methods=['POST'])
def predict_general():
    if request.is_json:
        data = request.get_json()
        features = [data['temp'], data['humidity'], data['pm2'], data['pm10'], data['no2'], data['so2'], data['co'], data['proximity'], data['populationDensity']]
        print(features)
        final_features = [np.array(features)]

        prediction = model.predict(final_features)
        if prediction[0] == 0:
            output = 'Good'
        elif prediction[0] == 1:
            output = 'Hazardious'
        elif prediction[0] == 2:
            output = 'Moderate'
        else:
            output = 'Poor'
        
        print(output)

        try:
            return render_template('result.html', prediction_text='Air Quality is {}'.format(output))
        except:
            print('error')
    else:
        print('error')


if __name__ == '__main__':
    app.run(debug=True)
