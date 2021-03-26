#import libraries
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify, url_for, redirect, render_template

#Flask constructor takes the name of current module (__name__) as argument.
app=Flask(__name__)

#Global variable - Load model, col list
model=joblib.load("model.pkl")
cols = ['variance', 'skewness', 'curtosis', 'entropy']

#Home route
@app.route('/')
def home():
  return render_template("home.html")

@app.route('/predict',methods=["Post"])
def predict_note_authentication():
  #variance,skewness,curtosis,entropy
  #Parse json post request
  req = request.get_json()
  input_data = req['data']
  input_data_df = pd.DataFrame.from_dict(input_data)
  
  #model prediction
  prediction = model.predict(input_data_df)
  
  #prediction
  if prediction[0] == 1.0:
    note_type = 'authentic'
  else:
    note_type = 'fake'
  
  #return to calling client
  return jsonify({'output':{'note_type':note_type}})

@app.route('/predictnotetype',methods=["Post"])
def predict_note_authentication2():
  #variance,skewness,curtosis,entropy
  #Parse json post request
  int_features = [x for x in request.form.values()]
  final = np.array(int_features)
  data_unseen = pd.DataFrame([final], columns = cols)

  #model prediction
  prediction = model.predict(data_unseen)
  
  #prediction
  if prediction[0] == 1.0:
    note_type = 'authentic'
  else:
    note_type = 'fake'
  
  #return to calling client
  return render_template('home.html',pred='Note is: {}'.format(note_type))
  #return note_type

#check if callable name is main
if __name__=='__main__':
  app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
    
