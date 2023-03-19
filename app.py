from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from datetime import date
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, FileField,SelectField,validators
from passlib.hash import sha256_crypt
from functools import wraps
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import RPi.GPIO as GPIO
import time

app=Flask(__name__)

#config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='iotproject'
app.config['MYSQL_CURSORCLASS']='DictCursor'

#init MySQL
mysql=MySQL(app)

def PIRSensor():
    pir=17
    sound=20
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir,GPIO.IN)
    GPIO.setup(sound,GPIO.OUT)
    while(True):
        temp=GPIO.input(pir)
        if(temp):
            print("No motion detected")
            GPIO.output(sound,GPIO.LOW)
        else:
            print("Motion detected")
            GPIO.output(sound,GPIO.HIGH)
    GPIO.cleanup()



class Login(Form):
    email=StringField('email')
    password=PasswordField('password')

@app.route('/',methods=['GET','POST'])
def login():
    form=Login(request.form)
    if(request.method=='POST'):
        email=request.form['email']
        password=request.form['password']
        if(email=='admin' and password=='admin'):
            return render_template('index.html')
    return render_template('login.html')

@app.route('/main',methods=['GET','POST'])
def index():
    return render_template('index.html')
   
@app.route('/pir',methods=['GET','POST'])
def pir():
    if(request.method=='POST'):
        check=request.form['submit1']
        if(check=="check"):
            PIRSensor()
    return render_template('pir.html')

def predict_crack():
    # Load the trained model
    model = load_model('crack_detection.h5')

    # Load the image to be classified
    img_path = '/home/iotlab/project/crack_test_images/cell0009.png'
    img = image.load_img(img_path, target_size=(300, 300), color_mode='grayscale')

    # Preprocess the image and convert it to a numpy array
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.

    # Predict the class of the image (cracked or uncracked)
    prediction = model.predict(x)
    print(prediction)
    if prediction[0][0] < prediction[0][1]:
        return 0
    else:
        return 1



@app.route('/crack',methods=['GET','POST'])
def crack():
    if(request.method=='POST'):
        check=request.form['submit1']
        if(check=="check"):
            res=predict_crack()
            #res=1
            return render_template('crack.html',res=res)
    return render_template('crack.html')


if __name__=='__main__':
    app.secret_key='123456'
    app.run(debug=True)
