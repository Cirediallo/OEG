import importlib
import time
import base64
import matplotlib.pyplot as plt
import resource
import gc

wikifier = importlib.import_module('display.wikifier')
wc = importlib.import_module('display.wc')
semantic = importlib.import_module('display.semantic')

get_related =  getattr(wikifier, "get_related")
get_semantics =  getattr(semantic, "get_semantics")
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

def generate_cloud_basic(text, conf_id, corpus=None, recent=None, language="en-US"):
    wc = generate_wc(text, corpus=corpus, recent=recent, language=language)
    wc.to_file(f"./conference_{conf_id}/cloud_{languages.get(language)}.png")

def wcs_save(wcs, conf_id, language, layout="radial"):
    fig = plt.figure()
    fig.set_size_inches(18, 15)
    
    coords = []
    if(layout == "radial"):
        gs = fig.add_gridspec(4, 4)
        coords= [gs[1:-1, 1:-1], gs[1, 0], gs[2, 3], gs[0, 1], gs[3, 2]]
    if(layout == "columns"):
        gs = fig.add_gridspec(3, 3)
        coords= [gs[0,0], gs[0, 1], gs[0, 2], gs[1, 0], gs[1,1], gs[1,2], gs[2,0], gs[2,1], gs[2,2]]
    
    for i in range(0, len(wcs)):
        ax = fig.add_subplot(coords[i])
        ax.axis('off')
        ax.imshow(wcs[i])

    plt.savefig(f"./conference_{conf_id}/cloud_{languages.get(language)}.png")
    plt.close(fig)

def generate_cloud_semantic(text, conf_id, corpus=None, recent=None, language="en-US"):
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
    wcs = generate_wcs_semantics(text_split_semantics, corpus=semantic.getCorpus(), recent=recent, semantic_fields=semantic.getSemanticFields(), language=language)
    wcs_save(wcs, conf_id, language, layout="radial")

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

        if(full != ""):
            if(corpus != ""):
                generate_cloud_semantic(full, conf_id, corpus=corpus, recent=recent, language=target)
            else:
                generate_cloud_basic(full, conf_id, corpus=corpus, recent=recent, language=target)            
            print(f"Generated cloud {languages.get(target)}")

    gc.collect()
    print(f"Memory used : {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")

    time.sleep(10)
    generate_conference_clouds(conf_id)


conf_id = input("Please enter conference id: ")
print("Conference identifier:", conf_id)
print("Starting generation")
generate_conference_clouds(conf_id)