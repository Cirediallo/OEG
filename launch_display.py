import importlib

wikifier = importlib.import_module('display.wikifier')
wc = importlib.import_module('display.wc')
semantic = importlib.import_module('display.semantic')

get_related =  getattr(wikifier, "get_related")
get_semantics =  getattr(semantic, "get_semantics")
wcs_plot =  getattr(wc, "wcs_plot")
wc_plot = getattr(wc, "wc_plot")
generate_wcs_semantics = getattr(wc, "generate_wcs_semantics")
generate_wc = getattr(wc, "generate_wc")

def generate_cloud_basic(text, corpus=None, recent=None, language="en-US"):
    return wc_plot(generate_wc(text, corpus=corpus, recent=recent, language=language))
    
def generate_cloud_semantic(text, corpus=None, recent=None, language="en-US"):
    
    r_fields, r_documents = get_related(corpus, language=language)
    
    corpus += " " + " ".join(r_documents)
    corpus
    semantic_fields = r_fields

    semantic_fields.append("Other")

    text_split_semantics = get_semantics(text, r_fields, r_documents, language=language)    
    
    return wcs_plot(generate_wcs_semantics(text_split_semantics, corpus=corpus, recent=recent, semantic_fields=semantic_fields, language=language), layout="radial")

def generate_conference_clouds(conf_name, language):    
    print("Début conf")
    fcorpus = open(f"./conference_{conf_name}/corpus.txt", "r")
    corpus = fcorpus.read() 
    fcorpus.close() 
    
    ftrans = open(f"./conference_{conf_name}/recent.txt", "r")
    recent = ftrans.read() 
    ftrans.close() 
    
    ftrans = open(f"./conference_{conf_name}/transcription.txt", "r")
    transcription = ftrans.read() 
    ftrans.close() 

    cloud = generate_cloud_basic(transcription, corpus=corpus, recent=recent, language=language)
    cloud.savefig(f"./conference_{conf_name}/cloud_{language}.png")
    print(f"cloud {language}")
    targets = ["ar-SA", "es-ES", "fr-FR", "en-US"]   
    for target in targets:
        if(target != language):          
            ftrad = open(f"./conference_{conf_name}/translated_{target}.txt", "r", encoding="utf-8")
            translation = ftrad.read() 
            ftrad.close() 
            
            ftrad = open(f"./conference_{conf_name}/recent_translated_{target}.txt", "r", encoding="utf-8")
            recent = ftrad.read() 
            ftrad.close() 
            cloud = generate_cloud_basic(translation, corpus=corpus, recent=recent, language=target)
            cloud.savefig(f"./conference_{conf_name}/cloud_{target}.png")
            print(f"cloud {target}")

    s.enter(10, 1, generate_conference_clouds, (conf_name, language))


import sched, time

s = sched.scheduler(time.time, time.sleep)
s.enter(10, 1, generate_conference_clouds, ("A2", "fr-FR"))
s.run()