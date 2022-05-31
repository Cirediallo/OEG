# -*- coding: utf-8 -*-
import importlib
import os
import re
import sys

import requests
import json

# Measure system ressource utilized by the program
import resource

import gc

from google.cloud import speech

"""
/* ==================== PROVIDE ==================== */
1. The credential path by defining the variable credential_path and affect it to the path of the credential
2. Point the environment variable "GOOGLE_APPLICATION_CREDENTIALS" to the credential
<code>
    os.environ[GOOGLE_APPLICATION_CREDENTIALS] = credential_path
</code>
3. Define the Project ID for translation as: 
PROJECT_ID = 'here_the_translation_project_id_from_gcp'
"""

translate_text =  getattr(importlib.import_module('speech.translate'), "translate_text")
ResumableMicrophoneStream  = getattr(importlib.import_module('speech.ResumableMicrophoneStreamClass'), 'ResumableMicrophoneStream')

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

"""
Terminal color code 
"""
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

PATH_FOLDER = './conferences'

"""
Iterates through server responses.
Get a sentence concatenation with word whose confidence level is above 70%

"""
def listen_print_loop(responses, stream):
    final = ""
    for response in responses:
        sentence = ""
        if not response.results:
            continue
            

        # Get a word when its stability is above 70% and add it to the current sentence
        if response.results[0].stability >= 0.70:
            sentence += " "+response.results[0].alternatives[0].transcript

        result = response.results[0]
        
        
        if not result.alternatives:
            continue
        
        transcript = result.alternatives[0].transcript

        if result.is_final:

            sys.stdout.write(GREEN)
            sys.stdout.write("\033[K")
            sys.stdout.write("transcription" + sentence + "\n")

            
            # Output of the transcription if one of the sentences matches one of the following keywords
            if re.search(r"\b(fin de la transcription|end of transcription|fin de transcripcion)\b", transcript, re.I):
                sys.stdout.write(YELLOW)
                sys.stdout.write("Exiting...\n")
                stream.closed = True
                break

            final += " " + transcript

        else:
            sys.stdout.write(RED)
            sys.stdout.write("\033[K")
            sys.stdout.write("transcript: " + transcript + "\r")

    return final            

# Languages
languages = {
    "arabic" : "ar-SA",
    "english" : "en-US",
    "french" : "fr-FR",
    "spanish" : "es-ES",
}
lang_targets = list(languages.keys())

"""
Send sentence to the website API route for database insertion
"""
def put_sentence(data):
    json_object = json.dumps(data, indent = 4, ensure_ascii=False).encode('utf8')
    print(json_object.decode())
    x = requests.post("https://multiling-oeg.univ-nantes.fr/insertion", data = json_object)
    print(x)

"""
Start bidirectional streaming from microphone input to Google Speech API and translate the sentence through the Translation API.
Write the transcription text and translation in each language file
Define current talk information
"""
def record_conference(conf_id, conf_name, conf_room, conf_lang):
    
    global PATH_FOLDER
    path = f'{PATH_FOLDER}/{conf_id}'
    if (os.path.exists(PATH_FOLDER) == False):
        os.mkdir(PATH_FOLDER)
    path = f'{PATH_FOLDER}/{conf_id}'
    if (os.path.exists(path) == False):
        os.mkdir(path)
    
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=languages.get(conf_lang),
        max_alternatives=1,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, Ctrl+C to stop.\n\n')
    sys.stdout.write("End (ms)       Transcript Results/Status\n")
    sys.stdout.write("=====================================================\n")

    with mic_manager as stream:

        while not stream.closed:
            sys.stdout.write(YELLOW)
            sys.stdout.write(
                "\n" + "NEW REQUEST\n"
            )

            stream.audio_input = []
            audio_generator = stream.generator()

            req = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, req, timeout=72000000)

            texts = {
                "english":"", 
                "french":"", 
                "spanish":"", 
                "arabic":""
            }

            transcription = listen_print_loop(responses, stream)
            
            if(transcription!=""):
                texts[conf_lang] = transcription
                for lang_target in lang_targets:
                    if(lang_target != conf_lang):
                        if(transcription != ""):
                            translation = translate_text(transcription, languages.get(conf_lang), languages.get(lang_target), PROJECT_ID)
                        else:
                            translation = transcription
                        texts[lang_target] = translation

                data = dict()
                data["conf_id"] = conf_id
                data["conf_name"] = conf_name
                data["conf_room"] = conf_room
                data["conf_lang"] = conf_lang
                data["sentences"] = texts.copy()
                
                put_sentence(data)

            for key, value in texts.items():
                if conf_lang == "arabic":
                    f = open(f"{path}/{key}_full.txt", "ab+")
                    if type(value) is bytes:
                        value = value
                    else:
                        value = value.encode('utf8')
                    f.write(" " + value)
                    f.close()

                    f2 = open(f"{path}/{key}_recent.txt", "wb+")
                    if type(value) is bytes:
                        value = value
                    else:
                        value = value.encode('utf8')
                    f2.write(" " + value)
                    f2.close()
                else:
                    f = open(f"{path}/{key}_full.txt", "a+", encoding="utf-8")
                    f.write(" " + value)
                    f.close()

                    f2 = open(f"{path}/{key}_recent.txt", "w+", encoding="utf-8")
                    f2.write(" " + value)
                    f2.close()

            print(f"Memory used : {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


def main():
    conf_id = input("Conference id: ")
    conf_title = input("Conference title: ")
    conf_lang=""
    while(conf_lang not in lang_targets):
        conf_lang = input("Conference language (arabic|english|french|spanish): ")

    print("Starting transcription")

    record_conference(conf_id, conf_title, "450", conf_lang)

if __name__== "__main__":
    main()