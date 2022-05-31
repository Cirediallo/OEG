# Open Education Global Multilingual  
### Description  
This projet is a multilingual project deployed at the Open Education Global 2022 Conference in Nantes. The goal is to break language barrier and allow a congres to be multilingual.   
The language taken into account this year is: Arabic, English, French, Spanish  
The application transcribe a voice streaming input of the current talk, translate the transcription and generate a word cloud based first on the abstract of the current talk and then on the transcribed and the translated text for each language supported.  
WordCloud generated, transcription and translation is send to the website API developped through a dictionnary which is stored in a Database.  
### Repository organisation: 
This repository have three branchs
- The main branch which is dedicated to the database  
- The oeg branch which is dedicated to the transcription, translation and wordcloud generation  
- The app branch which is dedicated to the website  
#### Technologies used:
The website have been developped using the micro Python frameword Flask  
The transcription and translation use google cloud APIs Speech-to-Text and Translate respectively  
The Word Cloud generation use the library wordcloud  
#### Challenges:

### Installation and Usage:  
This project can be used adaptively, you can use the word cloud generation part on its own, or you can use the transcription part on its ownn, or the translation part on its own or you can use them all together with another website by providing the website API routes where it's required.  
For sake of simplicity, you can use the website deployed with the application.  
For full installation install the requirement file using pip:   
`pip3 install -r requirements.txt`
For usage, in differents consoles run launch_speech.py and lauch_display.py
`python3 lauch_speech.py`
`python3 lauch_display.py`
Fill the information asked for current talk and here you go

### Licences: 
This project is CC BY  

