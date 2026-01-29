from flask import Flask, request
import pickle

app = Flask(__name__)

# Load model once (important)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.post('/predict')
def handle_post():
    if not request.form:
        return "Error: No form data received", 400

    try:
        features = [
            'OverallQual', 'GrLivArea', 'GarageCars',
            'TotalBsmtSF', 'YearBuilt', 'FullBath',
            'BedroomAbvGr', 'LotArea'
        ]

        input_data = [float(request.form[f]) for f in features]

        prediction = model.predict([input_data])

        return f"The predicted price of the house is {prediction[0]}"

    except KeyError as e:
        return f"Error: Missing form field {e}", 400

    except ValueError:
        return "Error: All input values must be numeric", 400

if __name__ == '__main__':
    app.run(port=8080, debug=True)