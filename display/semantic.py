import importlib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel     
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('wordnet')

commons = importlib.import_module('display.commons')
tokenize_text =  getattr(commons, "tokenize_text")
stop_words_en =  getattr(commons, "stop_words_en")
stop_words_fr =  getattr(commons, "stop_words_fr")
stop_words_ar =  getattr(commons, "stop_words_ar")
stop_words_es =  getattr(commons, "stop_words_es")


class LemmaTokenizer:
    ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.ignore_tokens]


def sentence_field(sentence, fields, documents, language="en-US"):
    tokenizer=LemmaTokenizer()
    
    if(language == "en-US"):
        stop_words = stop_words_en
    elif(language == "fr-FR"):
        stop_words = stop_words_fr 
    elif(language == "es-ES"):
        stop_words = stop_words_es 
    elif(language == "ar-SA"):
        stop_words = stop_words_ar
            
    token_stop = tokenizer(' '.join(stop_words))

    
    vectorizer = TfidfVectorizer(stop_words=token_stop, 
                                  tokenizer=tokenizer)
    doc_vectors = vectorizer.fit_transform([sentence] + documents)
    
    cosine_similarities = linear_kernel(doc_vectors[0:1], doc_vectors).flatten()
    document_scores = [item.item() for item in cosine_similarities[1:]]
    
    if(sum(document_scores) == 0): 
      return "Other"
    return fields[document_scores.index(max(document_scores))]

def get_semantics(sentences, fields, documents, language="en-US"):
  chunks = tokenize_text(sentences, language=language)
  fields.append("Other")
  text_dict = dict.fromkeys(fields)
  for chunk in chunks:
    field =  sentence_field(chunk, fields, documents, language=language)
    if(text_dict[field] == None):
      text_dict[sentence_field(chunk, fields, documents, language=language)] = chunk
    else:
      text_dict[sentence_field(chunk, fields, documents, language=language)] += " " + chunk
  return text_dict
