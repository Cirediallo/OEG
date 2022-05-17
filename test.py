import requests
import json
import base64
from PIL import Image
from io import BytesIO


"""
texts = {
    "english":"", 
    "french":"ça", 
    "spanish":"", 
    "arabic":"ادم ح"
}
            
data = dict()
data["conf_id"] = "10"
data["conf_name"] = "Name1"
data["conf_room"] = "Room1"
data["conf_lang"] = "french"
data["sentences"] = texts.copy()


json_object = json.dumps(data, indent = 4, ensure_ascii=False).encode('utf8')

r = requests.put("https://multiling-oeg.univ-nantes.fr/insertion", data = json_object)
#print(r)

t =json.loads(json_object.decode('utf-8'))
print(t)"""

import base64 

conf_id = "1"
languages = ["french", "spanish", "arabic", "english"]


images = {
    "english":"1", 
    "french":"2", 
    "spanish":"3", 
    "arabic":"4"
}


for language in languages:
    cloud = open(f'./conference_{conf_id}/cloud_{language}.png', 'rb')
    encoded = base64.b64encode(cloud.read())
    images[language] = encoded

print(images)
r = requests.post("https://multiling-oeg.univ-nantes.fr/updateWordCloud", data = images)
print(r)



