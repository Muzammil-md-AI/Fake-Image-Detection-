import requests,os,re
from flask import Flask,redirect,url_for,render_template,request
from werkzeug.utils import secure_filename           # Used to store filename
import cv2
from keras.models import load_model, model_from_json
from PIL import Image
import json
import numpy as np
import glob


# Load model from Json file
json_file = open('/Users/muzammil/Major/Fake_image_detection/model.json','r')
loaded_model = json_file.read()
json_file.close()
load_model = model_from_json(loaded_model)
load_model.load_weights('/Users/muzammil/Major/Fake_image_detection/model.h5')
removing_files = glob.glob('/Users/muzammil/Major/Fake_image_detection/static/uploads/*.jpg')
for i in removing_files:
        os.remove(i)

app=Flask(__name__)
@app.route("/")
def uploader():

        path = '/Users/muzammil/Major/Fake_image_detection/static/uploads/'
        uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))       
        print(uploads)
        uploads = ['uploads/' + file for file in uploads]
        uploads.reverse()
        return render_template("index.html",uploads=uploads)            

app.config['UPLOAD_PATH'] = '/Users/muzammil/Major/Fake_image_detection/static/uploads/'     # Storage path
@app.route("/upload",methods=['GET','POST'])
def upload_file():                                       # This method is used to upload files 
        removing_files = glob.glob('/Users/muzammil/Major/Fake_image_detection/static/uploads/*.jpg')
        for i in removing_files:
                os.remove(i)
        if request.method == 'POST':
                f = request.files['file']
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                # Load Image
                fname=r'/Users/muzammil/Major/Fake_image_detection/static/uploads/'+ filename
                
                image = Image.open(fname)
                
                im = image.resize((200,200))
                im = np.asarray(im)
                im = np.reshape(im,(1,im.shape[0],im.shape[1],im.shape[2]))

                # Make Prediction
                prediction = load_model.predict(im)
                if prediction == 1:
                        print('Real Face')
                        image.save("/Users/muzammil/Major/Fake_image_detection/static/uploads/Real_"+filename)
                else:
                        print('Fake Face')
                        image.save("/Users/muzammil/Major/Fake_image_detection/static/uploads/Fake_"+filename)
                        
        os.remove(fname)
        return redirect("/")           
if __name__=="__main__":
        app.debug=True
        app.run()
