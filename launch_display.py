# -*- coding: utf-8 -*-
import importlib
import time
import base64
import matplotlib.pyplot as plt
import resource
import gc
import requests
import signal

wc = importlib.import_module('display.wc')
generate_wc = getattr(wc, "generate_wc")

languages = {
    "ar-SA" : "arabic",
    "en-US" : "english",
    "fr-FR" : "french",
    "es-ES" : "spanish",
}

PATH_FOLDER = './conferences'

""" Generate word cloud image based on the abstract of the current talk """
def generate_cloud_basic(text, conf_id, corpus=None, recent=None, language="en-US"):
    global PATH_FOLDER
    path = f'{PATH_FOLDER}/{conf_id}'
    wc = generate_wc(text, corpus=corpus, recent=recent, language=language)
    wc.to_file(f"{path}/cloud_{languages.get(language)}.png")


def read_files(conf_id, target):
    global PATH_FOLDER
    path = f'{PATH_FOLDER}/{conf_id}'

    try:      
        f = open(f"{path}/{languages.get(target)}_full.txt", "r", encoding="utf-8")
        full = f.read() 
        f.close() 
    except FileNotFoundError:
        full = ""

    try: 
        f2 = open(f"{path}/{languages.get(target)}_recent.txt", "r", encoding="utf-8")
        recent = f2.read() 
        f2.close() 
    except FileNotFoundError:
        recent = ""

    try:
        f = open(f"{path}/corpus_{languages.get(target)}.txt", "r")
        corpus = f.read() 
        f.close() 
    except FileNotFoundError:
        corpus = ""

    return full, recent, corpus

"""
Send wordcloud images to the website API throught a post HTTP request and return error if an error occurred
"""
def post_wordcloud(conf_id):
    global PATH_FOLDER
    path = f'{PATH_FOLDER}/{conf_id}'

    error = False
    languages = ["french", "spanish", "arabic", "english"]
    images = {
        "english":"", 
        "french":"", 
        "spanish":"", 
        "arabic":""
    }
    for language in languages:
        try:
            f = open(f'{path}/cloud_{language}.png', 'rb')
            encoded = base64.b64encode(f.read())
            f.close()
            images[language] = encoded
        except FileNotFoundError:
            error = True
    if(error == False):
        time.sleep(1)
        r = requests.post("https://multiling-oeg.univ-nantes.fr/updateWordCloud", data = images)
        print(r)
        return r
    return "error"

"""
Generate the last wordcloud from the file containing recents sentences for each language
"""
def end_conference(conf_id): 
    lang_targets = ["ar-SA", "es-ES", "fr-FR", "en-US"]   
    for lang_target in lang_targets:
        full, recent, corpus = read_files(conf_id, lang_target)
        if(full != "" or corpus != ""):
            if(full == "") :
                generate_cloud_basic(corpus, conf_id, corpus=corpus, recent=corpus, language=lang_target)  
            elif(corpus != ""):
                generate_cloud_basic(full+corpus, conf_id, corpus=corpus, recent=full+corpus, language=lang_target)
            else:
                generate_cloud_basic(full, conf_id, corpus=corpus, recent=full, language=lang_target)            
            print(f"Generated cloud {languages.get(lang_target)}")
    
    status_code = 0
    while(status_code!=200):
        status_code = post_wordcloud(conf_id).status_code
        time.sleep(5)


""" Ctrl-C Signal handler """
def handler(signum, frame):
    res = input("Do you really want to end conference? y/n ")
    if res == 'y':
        end_conference(conf_id)
        exit(1)

""" Generate word cloud image of the current talk """

def generate_conference_clouds(conf_id):  
    signal.signal(signal.SIGINT, handler)  
    lang_targets = ["ar-SA", "es-ES", "fr-FR", "en-US"]   
    for lang_target in lang_targets:
        full, recent, corpus = read_files(conf_id, lang_target)

        if(full != "" or corpus != ""):
            if(full == "") :
                generate_cloud_basic(corpus, conf_id, corpus=corpus, recent="", language=lang_target)  
            elif(corpus != ""):
                generate_cloud_basic(full+corpus, conf_id, corpus=corpus, recent=recent, language=lang_target)   
            else:
                generate_cloud_basic(full, conf_id, corpus=corpus, recent=recent, language=lang_target)            
            print(f"Generated cloud {languages.get(lang_target)}")

    post_wordcloud(conf_id)

    gc.collect()
    print(f"Memory used : {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")

    time.sleep(5)
    generate_conference_clouds(conf_id)


def main():
    
    conf_id = input("Conference id: ")
    print("Starting generation")

    generate_conference_clouds(conf_id)

if __name__== "__main__":
    main()