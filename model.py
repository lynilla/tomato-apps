from PIL import Image
from numpy import asarray
# import tensorflow as tf
import logging
import numpy as np
import json
import requests


SIZE=256
MODEL_URI='https://tomato-densenet.herokuapp.com/v1/models/tomato_densenet:predict'
CLASSES = ["Bacterial Spot","Early Blight","Late Blight","Leaf Mold","Septoria Leaf Spot","Spider Mites","Target Spot","Yellow Leaf Curl Virus","Mosaic Virus","Healthy"]

# logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
# handler = logging.FileHandler('test.log') # creates handler for the log file
# logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

def get_prediction(image_path):    
    image =  np.array(Image.open(image_path).resize((SIZE,SIZE)))    
    img = asarray(image)
    img = img.reshape(1, 256, 256, 3)
    img = img.astype('float32')
    img = img / 255.0


    mydata = json.dumps({
        'instances': img.tolist()
    })

    response = requests.post(MODEL_URI , data=mydata)
    # print(response.json())
    result = json.loads(response.text)
    predictionList = result['predictions'][0]
    # logger.info(result['predictions'][0])
    predictionIdx = predictionList.index(max(predictionList))
    return {"class_name":CLASSES[predictionIdx] , "percentage":max(predictionList)}


# img = asarray(image)
# img = img.reshape(1, 256, 256, 3)
# img = img.astype('float32')
# img = img / 255.0

# mydata = json.dumps({
#     'instances': img.tolist()
# })
# response = requests.post(MODEL_URI , data=mydata)
# # print(response.json())
# result = json.loads(response.text)
# predictionList = result['predictions'][0]
# predictionIdx = predictionList.index(max(predictionList))
# print(CLASSES[predictionIdx])