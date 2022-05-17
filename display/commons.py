import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re
import math

nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words_en = set(stopwords.words('english'))
stop_words_fr = set(stopwords.words('french'))
stop_words_ar = set(stopwords.words('arabic'))
stop_words_es = set(stopwords.words('spanish'))

def tokenize_text(text, language="en-US"): 
  if(language == "en-US"):
      stop_words = stop_words_en
  elif(language == "fr-FR"):
      stop_words = stop_words_fr 
  elif(language == "es-ES"):
      stop_words = stop_words_es 
  elif(language == "ar-SA"):
      stop_words = stop_words_ar
      
  return [
    word 
    for word in re.split("\W+", text.lower())
    if word not in stop_words and len(word)>1 and word.isnumeric() == False and word.isalnum() == True
  ]

def get_freqDist(text, corpus=None, language="en-US"):
  freqDist = FreqDist()
  for word in tokenize_text(text, language=language):
        freqDist[word] += 1

  if(corpus != None):
    return ponderate_freqDist(freqDist, corpus)
  return freqDist

def ponderate_freqDist(freqs, corpus):
  corpusFreqs = get_freqDist(corpus)
  D = 1 + len(corpusFreqs)
  freqDist = FreqDist()
  for word in freqs:
    tf = 0.4+0.6*(freqs.freq(word)/freqs.freq(freqs.max()));#Normalized to max
    df = 1 + int(corpusFreqs.freq(word)>0)
    idf = math.log(D/df)
    freqDist[word] = tf*idf + 0.000001
  return freqDist
