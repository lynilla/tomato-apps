from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap

import os
import model
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime


app = Flask(__name__, template_folder='Template')
Bootstrap(app)
port = int(os.environ.get("PORT", 5000))

"""
Firebase
"""
# Initialize Firestore DB
cred = credentials.Certificate(
    "bangkit-finalproject-firebase-adminsdk-v8dc7-218c11fe14.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
tomato_ref = db.collection('bangkit_tomato')

"""
Routes
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    now_timestamp = datetime.now()
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            image_path = os.path.join('static', uploaded_file.filename)
            uploaded_file.save(image_path)
            rs = model.get_prediction(image_path)
            result = {
                'class_name': rs["class_name"],
                'percentage': rs["percentage"],
                'image_path': image_path,
            }

            filename_data_save = image_path
            predict_class = rs["class_name"]
            percentage = rs["percentage"]

            tomato_ref.document().set({'percentage': percentage, 'predict_class': predict_class,
                                       'file_path': filename_data_save, 'timestamp': str(datetime.timestamp(now_timestamp))})
       
            return render_template('result.html', result=result)

    query = tomato_ref.order_by(
        'timestamp', direction=firestore.Query.DESCENDING).limit(5)

    results = query.stream()
    data_dict_history = {}

    for doc in results:
        data_dict_history[doc.get('timestamp')] = [doc.get(
            'file_path'), doc.get('predict_class'), doc.id,doc.get('percentage')]

    return render_template('index.html', result_dict=data_dict_history)


@app.route('/predict', methods=['GET'])
def predict():
    return render_template('predict.html')


@app.route('/mini_encyclopedia/<topics>', methods=['GET'])
def encyclopedia(topics):
    if topics == 'SpiderMites':
        return render_template('encylopedia_spidermites.html')
    elif topics == 'BacterialSpot':
        return render_template('encylopedia_bacterialspot.html')
    elif topics == 'EarlyBlight':
        return render_template('encylopedia_earlyblight.html')
    elif topics == 'YellowLeafCurlVirus':
        return render_template('encylopedia_yellowleafcurlvirus.html')
    elif topics == 'LateBlight':
        return render_template('encylopedia_lateblight.html')
    elif topics == 'LeafMold':
        return render_template('encylopedia_leafmold.html')
    elif topics == 'SeptoriaLeafSpot':
        return render_template('encylopedia_septorialeafspot.html')
    elif topics == 'TargetSpot':
        return render_template('encylopedia_targetspot.html')
    elif topics == 'MosaicVirus':
        return render_template('encylopedia_mosaicvirus.html')
    elif topics == 'Healthy':
        return render_template('encylopedia_healthy.html')
    elif topics == 'General':
        return render_template('encylopedia.html')
    else:
        return 'request cannot be handled'


@app.route('/report/<id>', methods=['GET'])
def report(id):
    print(id)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
