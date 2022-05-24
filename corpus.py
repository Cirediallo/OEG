"""
This script is meant to generate some corpuses out of a CSV file
Dependant on specific files, not meant to be used on every projects
"""

import csv
import os
import importlib

translate_text = getattr(importlib.import_module('speech.translate'), "translate_text")

credential_path = "./speech/speechtotextapi.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
API_PROJECT_ID = 'starry-will-351113'

PATH_FOLDER = './conferences'

with open('./confs.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)#Skip header
    for row in csv_reader:
        conf_id = row[0]
        conf_lang = row[5]
        conf_corpus = row[6]

        path = f'{PATH_FOLDER}/{conf_id}'
        if (os.path.exists(PATH_FOLDER) == False):
            os.mkdir(PATH_FOLDER)
        path = f'{PATH_FOLDER}/{conf_id}'
        if (os.path.exists(path) == False):
            os.mkdir(path)

        f = open(f"{path}/corpus_{conf_lang}.txt", "w+", encoding="utf-8")
        f.write(f"{conf_corpus}")
        f.close()

        languages = {
            "arabic" : "ar-SA",
            "english" : "en-US",
            "french" : "fr-FR",
            "spanish" : "es-ES",
        }
        lang_targets = list(languages.keys())

        for lang_target in lang_targets:
            if(conf_lang != lang_target):
                trad_corpus = translate_text(conf_corpus, languages.get(conf_lang), languages.get(lang_target), API_PROJECT_ID)
                f = open(f"{path}/corpus_{lang_target}.txt", "w+", encoding="utf-8")
                f.write(f"{trad_corpus}")
                f.close()

        print(path)