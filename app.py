from flask import Flask, render_template,flash,redirect,url_for,session,logging,request,jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, FileField,SelectField,validators
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
#import RPi.GPIO as GPIO
import datetime

from PIL import Image

app=Flask(__name__)


#init MySQL
# mysql=MySQL(app)

#config MySQL
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']=''
# app.config['MYSQL_DB']='major_project'
# app.config['MYSQL_CURSORCLASS']='DictCursor'

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


res1,res2,res3='','',''

# Load the crack_ML model
crack_model = load_model('crack_detection.h5')


def predict_crack(img):
    # Preprocess the image and convert it to a numpy array
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.

    # Predict the class of the image (cracked or uncracked)
    prediction = crack_model.predict(x)
    print(prediction)
    if prediction[0][0] < prediction[0][1]:
        return "The Panel is not cracked"
    else:
        return "The Panel is cracked"


def c_predict():
    # Get the uploaded image file
    file = request.files['file']

    print(file)
    # Preprocess the image
    img = Image.open(file)
    #predict_crack(img)    
    img = img.resize((300, 300))
    #img = img.convert("L")
    res1=predict_crack(img)
    print('res: ',res1)
    return res1 #render_template('index.html',res=res)


# Load the dust_ML model
dust_model = load_model('dust_detection.h5')

def predict_dust(img):
   # Convert the image to a numpy array
    img_array = image.img_to_array(img)

    # Add a batch dimension to the image
    img_array = np.expand_dims(img_array, axis=0)

    # Normalize the pixel values
    img_array = img_array / 255.

    # Predict whether the image is dusty or clean
    prediction = dust_model.predict(img_array)
    
    print(prediction)
    if prediction > 0.5:
        return 'The image is dusty'
    else:
        return 'The image is clean'


def d_predict():

    file = request.files['file']
    # Get the uploaded image file
    img = Image.open(file)

    # Resize the image to the desired shape
    img = img.resize((250, 290))

    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Expand the dimensions of the array to match the expected shape
    img_array = np.expand_dims(img_array, axis=0)

    #res2=predict_dust(img_array)

    # Pass the image array to the model for prediction
    prediction = dust_model.predict(img_array)
    print(prediction)
    if prediction > 0.5:
        res2= 'The image is dusty'
    else:
        res2= 'The image is clean'
    print('res: ',res2)
    return res2 #render_template('index.html',res=res)
'''
@app.route('/notifications', methods=['POST'])
def notifications():
    if request.method=='POST':
        cur=mysql.connection.cursor()

        res=cur.execute("SELECT * FROM notifications")
        notification=cur.fetchall()
        if request.form['submit']=='crack':
            res1=c_predict()
            print(res1)
            ct = datetime.datetime.now()
            cur.execute("INSERT INTO notifications(option,message,timestamp) VALUES(%s,%s,%s)",('Crack',res1,ct))
        elif request.form['submit']=='dust':
            res2=d_predict()
            print(res2)
            ct = datetime.datetime.now()
            cur.execute("INSERT INTO notifications(option,message,timestamp) VALUES(%s,%s,%s)",('Dust',res2,ct))
        elif request.form['submit']=='pir':
            ct = datetime.datetime.now()
            cur.execute("INSERT INTO notifications(option,message,timestamp) VALUES(%s,%s,%s)",('Bird',res3,ct))
        
        mysql.connection.commit()  
        res=cur.execute("SELECT * FROM notifications")
        notification=cur.fetchall()  
        cur.close()

        return render_template('notifications.html',res=res,notification=notification)

'''

if __name__=='__main__':
    app.secret_key='123456'
    app.run(debug=True)
