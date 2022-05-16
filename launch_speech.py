import importlib
import os
import re
import sys
from google.cloud import speech

import requests
import json

credential_path = "./speech/speechtotextapi.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

translate_text =  getattr(importlib.import_module('speech.translate'), "translate_text")
ResumableMicrophoneStream  = getattr(importlib.import_module('speech.ResumableMicrophoneStreamClass'), 'ResumableMicrophoneStream')


SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


def listen_print_loop(responses, stream, language):
    final = ""
    for response in responses:
        sentence = ""
        if not response.results:
            continue
        else:
            """
            print("------------------QUE CACHE RESPONSE ---------------------")
            print(response)
            #sentence = response.
            print("----------------- FIN RESPONSE --------------------------")
            print("================= PRINTING RESPONSE RESULTS ===============")
            print(response.results[0])
            """
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

            if re.search(r"\b(sortir de là|end of transcription|propaganda)\b", transcript, re.I):
                sys.stdout.write(YELLOW)
                sys.stdout.write("Exiting...\n")
                stream.closed = True
                break

            final += transcript

        else:
            sys.stdout.write(RED)
            sys.stdout.write("\033[K")
            sys.stdout.write("transcript: " + transcript + "\r")

    return final            

targets = ["ar-SA", "es-ES", "fr-FR", "en-US"]

def record_conference(conf_name, source="en-US"):
    
    path = f'conference_{conf_name}'
    if (os.path.exists(path) == False):
        os.mkdir(path)
    
    
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=source,
        
        max_alternatives=1,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
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

            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests, timeout=72000000)

            transcription = listen_print_loop(responses, stream, source)
            
            #write transcription
            if source != "ar-SA":
                ftrans = open(f"./conference_{conf_name}/transcription.txt", "a+")
                ftrans.write("{}".format(transcription))
                ftrans.close()
                
                ftrans = open(f"./conference_{conf_name}/recent.txt", "w+")
                ftrans.write("{}".format(transcription))
                ftrans.close()
            else:
                ftrans = open(f"./conference_{conf_name}/transcription.txt", "ab+")
                transcription = transcription.encode("utf-8")
                ftrans.write(transcription)
                ftrans.close()
                
                ftrans = open(f"./conference_{conf_name}/recent.txt", "wb+")
                transcription = transcription.encode("utf-8")
                ftrans.write(transcription)
                ftrans.close()
            
            #do and write translation
            for target in targets:
                if(target != source):
                    if(transcription != ""):
                        translation = translate_text(transcription, source=source, target=target)
                    else:
                        translation = transcription
                        
                    ftrad = open(f"./conference_{conf_name}/translated_{target}.txt", "a", encoding="utf-8")
                    ftrad.write(" " + translation)
                    ftrad.close()
                    
                    ftrad = open(f"./conference_{conf_name}/recent_translated_{target}.txt", "w", encoding="utf-8")
                    ftrad.write(translation)
                    ftrad.close()
                

record_conference("A2", source="fr-FR")