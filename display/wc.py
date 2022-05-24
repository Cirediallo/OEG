# -*- coding: utf-8 -*-
import importlib
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

commons = importlib.import_module('display.commons')
tokenize_text =  getattr(commons, "tokenize_text")
get_freqDist =  getattr(commons, "get_freqDist")
stop_words =  getattr(commons, "stop_words")

class SimpleGroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)

def recent_word_color_func(color="blue", light_color="lightblue", recent=None):
  if(recent==None) : return None

  color_to_words = {
      color : tokenize_text(recent)
  }

  return SimpleGroupedColorFunc(color_to_words, light_color)


def generate_wcs_semantics(splits, corpus, recent, semantic_fields, language="en-US"):
    colors = ["blue", "limegreen", "red", "purple", "darkorange"]
    lightcolors = ["lightblue", "lightgreen", "lightcoral", "thistle", "bisque"]
    wcs = []

    x, y = np.ogrid[:900, :900]
    mask = (x - 450) ** 2 + (y - 450) ** 2 > 450 ** 2
    mask = 255 * mask.astype(int)

    if(language == "ar-SA"):
        font_path ='./display/fonts/ARIAL.TTF'
    else:
        font_path="./display/fonts/NotoSans-Regular.ttf"

    nb_bins = []#Order wc by size
    
    for key in splits:
      if(splits[key] != None):
        freqs = get_freqDist(splits[key], corpus, language=language)
    
        nb_bins.append(freqs.B()+semantic_fields.index(key)*0.001)#Prevents same values
    
        wcs.append(WordCloud(max_words=20,
                             font_path=font_path,
                             stopwords=stop_words,
                             prefer_horizontal=1, 
                             mode="RGBA",
                             background_color=None, 
                             color_func=recent_word_color_func(colors[semantic_fields.index(key)], lightcolors[semantic_fields.index(key)], recent),
                             mask = mask
                    ).generate_from_frequencies(freqs))
    
    sorted_freqs= sorted(nb_bins, reverse=True)
    sorted_order = [sorted_freqs.index(freq) for freq in nb_bins]
    zipped_lists = zip(sorted_order, wcs)
    sorted_zipped_lists = sorted(zipped_lists)
    wcs = [element for _, element in sorted_zipped_lists]
    return wcs

def generate_wc(text, corpus=None, recent=None, language="en-US"):
    x, y = np.ogrid[:900, :900]
    mask = (x - 450) ** 2 + (y - 450) ** 2 > 450 ** 2
    mask = 255 * mask.astype(int)

    freqs = get_freqDist(text, corpus, language=language)  

    if(recent != None):
        color_func = recent_word_color_func("#188aff", "lightblue", recent)
    else :
        color_func = None
    
    if(language == "ar-SA"):
        font_path ='./display/fonts/ARIAL.TTF'
    else:
        font_path="./display/fonts/NotoSans-Regular.ttf"

    wc = WordCloud(max_words=20,
             font_path=font_path,
             stopwords=stop_words,
             prefer_horizontal=1, 
             mode="RGBA",
             background_color=None, 
             color_func=color_func,
             mask = mask
             ).generate_from_frequencies(freqs)
    
    return wc