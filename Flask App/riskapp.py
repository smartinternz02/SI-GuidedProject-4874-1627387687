import numpy as np
from flask import Flask, request, jsonify, render_template
import requests
import json

API_KEY = "VDTCF49MO0QvZnruXmP3TdiJa_80mKvqdYb4OqYr8dFL"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken", mltoken)
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)  # interfacee between by server and my application wsgi


@app.route('/')  # bind to an url 
def home():
    return render_template("index.html")


@app.route('/login', methods=['POST'])  # bind to an url 
def admin():
    u = request.form["age"]
    v = request.form["gen"]
    a = request.form["js"]
    b = request.form["hs"]
    c = request.form["sa"]
    d = request.form["ca"]
    e = request.form["cra"]
    f = request.form["dh"]
    # Note while passing t see the order of dataset
    t = [[int(f), int(e), int(d), int(c), int(b), int(a), int(v), int(u)]]
    payload_scoring = {"input_data": [{"field": [
        ["Age", "Gender", "Job Status", "Housing Type", "Savings Account", "Checking Account", "Credit Amount",
         "Duration In Hours"]],
        "values": t}]}
    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/924f4dcc-40b5-4990-b90b-ac4f7c0d6937/predictions?version=2021-08-05',
        json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if (pred == 0):
        output = "There's a Risk in Allocating Loan to him"
    else:
        output = "There's No Risk in Allocating Loan to Him"
    return render_template('index.html', prediction_text=output)


if __name__ == "__main__":
    app.run(debug=True)