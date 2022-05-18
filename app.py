from flask import Flask, render_template, request, jsonify
from urllib.request import urlretrieve
import wave, struct
import json
import js2py
import re
import os as os

import base64


import my_python.word_cloud_generation.word_cloud_generation as word_cloud_generation
import my_python.api.conf_manager as ConfManager
import my_python.manager.cache_data_manager as CacheDataManager
import my_python.api.likeSystem as likeSystem
import my_python.const.lang_const as LangConst

#import jsonpickle
#import numpy as np
#import cv2

app = Flask(__name__, template_folder='templates')
app.debug = True


#app.run(ssl_context="adhoc")

## Welcome page ::

@app.route('/')
def root():
    return render_template('index.html')


## Welcome page ::

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


## The app's html view ::

@app.route('/view')
def view():
    return render_template('view.html')


## The app's solution

@app.route("/update", methods=['POST'])
def update():
    text = request.form['text']
    language = request.form['lang']
    word_cloud_generation.getCloudFromTextAndLanguage(text, language)
    return render_template('record.html')



@app.route("/sentences", methods=['GET'])
def sentences():
    print(request.form, request.args)
    num_sentence = int(request.args.get('nb_sentence'))
    room = int(request.args.get('room'))
    lang = request.args.get('lang')

    sentences = CacheDataManager.getDisplayed_sentences_room_language_from(room, lang, num_sentence)
    return jsonify({'sentences': sentences})



########### Likes ###############

@app.route("/likeSentence", methods=['POST'])
def LikeSentence():
    likeSystem.LikeSentence(request)
    return render_template('view.html')

@app.route("/UnlikeSentence", methods=['POST'])
def UnlikeSentence():
    likeSystem.UnlikeSentence(request)
    return render_template('view.html')

################################


@app.route("/mostly_liked_sentences", methods=['GET'])
def Mostly_liked_sentences_api():
    room = int(request.args.get('room'))
    return likeSystem.Mostly_liked_sentences(room)

@app.route("/startConf", methods=['POST'])
def startConf():
    room = int(request.form.get('room'))
    lang = request.form.get('lang')
    ConfManager.startConf(room, lang)
    return render_template('index.html')

@app.route("/stopConf", methods=['POST'])
def stopConf():
    room = int(request.form.get('room'))
    ConfManager.setConf_questions_state(room)
    return render_template('index.html')

@app.route("/endConf", methods=['POST'])
def endConf():
    room = int(request.form.get('room'))
    ConfManager.endConf(room)
    return render_template('index.html')



@app.route("/updateWordCloud", methods=['POST'])
def updateWordCloud():
    #request.get_json()
    #print(request.get_json(force=True))
    #cloud = request.get_json(force=True)['WC']
    #
    #print(cloud)
    #cloud_data = base64.b64decode(cloud)
    #print(cloud_data)
    #name = request.form['name']

    values = request.form

    #path = "/var/www/html/multilingOEG22/static/exposed"
    path = "./static/exposed"

    # Bytes to string
    #mem = ''.join(map(chr, mem))
    # String to json
    #mem = '"'.join(mem.split("'"))
    # Json to dictionnary
    #values = json.loads(mem)

    for k,v in values.items():
        decoded = base64.b64decode(v)
        lang = LangConst.REVERSE_MATCHER[k]
        image_result = open(f'{path}/word_cloud.{lang}.png', 'wb')
        image_result.write(decoded)

    #if os.path.exists(name):
    #    os.remove(name)
    #print('plante ici')
    # convert string of image data to uint8
    #nparr = np.fromstring(request.data, np.uint8)
    #print('ou là')
    # decode image
    #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    #print(img)
    #print(type(img))
    # encode response using jsonpickle
    #response_pickled = jsonpickle.encode(response)


    return render_template('index.html')







@app.route("/insertion", methods=['PUT'])
def SentenceInsertion():
    values = request.data
    # Bytes to string
    values = values.decode('utf8')
    #values = ''.join(map(chr, mem))
    # String to json
    #values = '"'.join(mem.split("'"))
    # Json to dictionnary
    values = json.loads(values)
    print (values)

    conf_id = int(values['conf_id'])
    conf_name = values['conf_name']
    conf_room = values['conf_room']
    conf_lang = values['conf_lang']
    eng_sentence = values['sentences'][LangConst.TRAD_ENGLISH]
    fr_sentence = values['sentences'][LangConst.TRAD_FRENCH]
    esp_sentence = values['sentences'][LangConst.TRAD_SPANISH]
    ara_sentence = values['sentences'][LangConst.TRAD_ARAB]

    return jsonify({'status_code': '200'})



if __name__== '__main__':
    app.run()