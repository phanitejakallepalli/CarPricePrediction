#importing all the required packages and libraries
from flask import Flask,render_template,request,redirect,url_for
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np
import db
import json


app=Flask(__name__)

cors=CORS(app)
#loading model
model=pickle.load(open('LinearRegressionModel.pkl','rb'))
#reading the csv file


car=pd.read_csv('Cleaned_Car_data.csv')
@app.route('/home')
def home():
    return render_template('main.html')
@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/submit', methods = ['POST'])
def signinp():
    status, username = db.check_user()

    #data = {
    #    "username": username,
    #   "status": status
    #}

    #return json.dumps(data)
    if status:
        return redirect(url_for('home'))
    
    return "Oops"

@app.route('/register', methods = ['POST'])
@cross_origin()
def register():
    status = db.insert_data()
    if status:
         return redirect(url_for('signin'))
    
    return redirect(url_for('signin'))
       
    
@app.route('/predict',methods=['GET'])
def index():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('index.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)


@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():

    company=request.form.get('company')

    car_model=request.form.get('car_models')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=request.form.get('kilo_driven')
   

    prediction=model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],data=np.array([car_model,company,year,driven,fuel_type]).reshape(1, 5)))
    print(prediction)
    #return "Hell"
    return str(np.round(prediction[0],2))
  
if __name__=='__main__':
    app.run(debug=True)