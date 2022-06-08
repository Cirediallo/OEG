# Open Education Global Multilingual  
### Description  
This projet is a multilingual project deployed at the [Open Education Global 2022 Conference](https://www.oeglobal.org/) in Nantes. The goal is to break language barrier and allow a congres to be multilingual.   
The language taken into account this year is: *Arabic*, *English*, *French*, *Spanish*  
The [application](https://multiling-oeg.univ-nantes.fr/) transcribe a voice streaming input of the current talk, translate the transcription and generate a word cloud based first on the abstract of the current talk and then on the transcribed and the translated text for each language supported.  
WordCloud generated, transcription and translation is send to the website API developped through a dictionnary which is stored in a Database.  
### Repository organisation: 
This repository have three branchs
- The main branch which is dedicated to the database  
- The oeg branch which is dedicated to the transcription, translation and wordcloud generation  
- The app branch which is dedicated to the website  
#### Technologies used:
The website have been developped using the micro Python frameword [Flask](https://flask.palletsprojects.com/en/2.1.x/)  
The transcription and translation use google cloud APIs [Speech-to-Text](https://cloud.google.com/speech-to-text/docs/before-you-begin) and [Translate](https://cloud.google.com/translate/docs/setup?hl=fr) respectively  
The Word Cloud generation use the library wordcloud  
#### Requirement: 
python >= 3.7

### Installation and Usage:  
This project can be used adaptively, you can use the word cloud generation part on its own, or you can use the transcription part on its ownn, or the translation part on its own or you can use them all together with another website by providing the website API routes where it's required.  
For sake of simplicity, you can use the website deployed with the application.  
For installation:  
* ###### Transcription, Translation and wordcloud
    * install the requirement file using pip:   
        `pip3 install -r requirements.txt`   
    * For usage, in differents consoles run launch_speech.py and lauch_display.py  
        `python3 lauch_speech.py`  
        `python3 lauch_display.py`  
    * Fill the information asked for current talk and here you go  
* ###### Website        
    *** For installation use: ***     
    * Unix:    
        `./setup.sh`   
    * Windows:    
        `./setup.psl`    
    *** For Usage, run: ***   
    * Unix:   
        `./run.sh`   
    * Windows:    
        `./run.psl`        
    
### Licences: 
This project is [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)  

