import requests
import json

texts = {
    "english":"Welcome", 
    "french":"Bienvenue", 
    "spanish":"Bienvenido", 
    "arabic":"أهلا بك"
}
            
data = dict()
data["conf_id"] = "OPENING"
data["conf_name"] = "Opening Ceremony"
data["conf_room"] = "Auditorium 450"
data["conf_lang"] = "english"
data["sentences"] = texts.copy()


json_object = json.dumps(data, indent = 4, ensure_ascii=False).encode('utf8')

r = requests.post("https://multiling-oeg.univ-nantes.fr/insertion", data = json_object)
print(r)