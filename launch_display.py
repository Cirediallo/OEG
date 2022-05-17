import importlib
import time

wikifier = importlib.import_module('display.wikifier')
wc = importlib.import_module('display.wc')
semantic = importlib.import_module('display.semantic')

get_related =  getattr(wikifier, "get_related")
get_semantics =  getattr(semantic, "get_semantics")
wcs_plot =  getattr(wc, "wcs_plot")
wc_plot = getattr(wc, "wc_plot")
generate_wcs_semantics = getattr(wc, "generate_wcs_semantics")
generate_wc = getattr(wc, "generate_wc")

languages = {
    "ar-SA" : "arabic",
    "en-US" : "english",
    "fr-FR" : "french",
    "es-ES" : "spanish",
}

semantic_french = None
semantic_spanish = None
semantic_arabic = None
semantic_english = None

class SemanticWrapper:
    def __init__(self, corpus, language):
        self.r_fields, self.r_documents = get_related(corpus, language=language)
        self.corpus = corpus + " " + " ".join(self.r_documents)
        self.semantic_fields = self.r_fields.copy()
        self.semantic_fields.append("Other")
        print(self.semantic_fields)
    def getCorpus(self):
        return self.corpus
    def getRelatedDocuments(self):
        return self.r_documents
    def getRelatedFields(self):
        return self.r_fields
    def getSemanticFields(self):
        return self.semantic_fields

def generate_cloud_basic(text, corpus=None, recent=None, language="en-US"):
    return wc_plot(generate_wc(text, corpus=corpus, recent=recent, language=language))
    

def generate_cloud_semantic(text, corpus=None, recent=None, language="en-US"):
    global semantic_french
    global semantic_spanish
    global semantic_arabic
    global semantic_english

    if(language == "en-US" and semantic_english==None):
        semantic_english = SemanticWrapper(corpus, language)
    if(language == "fr-FR" and semantic_french==None):
        semantic_french = SemanticWrapper(corpus, language)
    if(language == "es-ES" and semantic_spanish==None):
        semantic_spanish = SemanticWrapper(corpus, language)
    if(language == "ar-SA" and semantic_arabic==None):
        semantic_arabic = SemanticWrapper(corpus, language)

    if(language == "en-US"):
        semantic = semantic_english
    if(language == "fr-FR"):
        semantic = semantic_french
    if(language == "es-ES"):
        semantic = semantic_spanish
    if(language == "ar-SA"):
        semantic = semantic_arabic

    text_split_semantics = get_semantics(text, semantic.getRelatedFields(), semantic.getRelatedDocuments(), language=language)    
    
    return wcs_plot(generate_wcs_semantics(text_split_semantics, corpus=semantic.getCorpus(), recent=recent, semantic_fields=semantic.getSemanticFields(), language=language), layout="radial")

def generate_conference_clouds(conf_id):    
    targets = ["ar-SA", "es-ES", "fr-FR", "en-US"]   
    for target in targets:
        try:      
            f = open(f"./conference_{conf_id}/{languages.get(target)}_full.txt", "r", encoding="utf-8")
            full = f.read() 
            f.close() 
        except FileNotFoundError:
            full = ""

        try: 
            f2 = open(f"./conference_{conf_id}/{languages.get(target)}_recent.txt", "r", encoding="utf-8")
            recent = f2.read() 
            f2.close() 
        except FileNotFoundError:
            recent = ""

        try:
            f = open(f"./conference_{conf_id}/corpus_{languages.get(target)}.txt", "r")
            corpus = f.read() 
            f.close() 
        except FileNotFoundError:
            corpus = ""
        
        if(corpus != ""):
            cloud = generate_cloud_semantic(full, corpus=corpus, recent=recent, language=target)
        else:
            cloud = generate_cloud_basic(full, corpus=corpus, recent=recent, language=target)
        
        if(full != ""):
            cloud.savefig(f"./conference_{conf_id}/cloud_{languages.get(target)}.png")
            print(f"Generated cloud {languages.get(target)}")

    time.sleep(10)
    generate_conference_clouds("A1")

generate_conference_clouds("A1")