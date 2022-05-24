# -*- coding: utf-8 -*-
import urllib.parse, urllib.request, json
import requests

def wikify(text, lang="auto", threshold=0.83):
  # Prepare the URL.
  data = urllib.parse.urlencode([
    ("text", text), ("lang", lang),
    ("userKey", "qjjgwwjyilpffjyyjczftfrfmyvlcu"),
    ("pageRankSqThreshold", "%g" % threshold), ("applyPageRankSqThreshold", "true"),
    ("nTopDfValuesToIgnore", "200"), ("nWordsToIgnoreFromList", "200"),
    ("wikiDataClasses", "true"), ("wikiDataClassIds", "false"),
    ("support", "true"), ("ranges", "false"), ("minLinkFrequency", "2"),
    ("includeCosines", "false"), ("maxMentionEntropy", "3")
    ])
  url = "http://www.wikifier.org/annotate-article"
  # Call the Wikifier and read the response.
  req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
  with urllib.request.urlopen(req, timeout = 60) as f:
    response = f.read()
    response = json.loads(response.decode("utf8"))
  # Output the annotations.
  return [annotation["title"] for annotation in response["annotations"]][0:4]

def get_wikipedia_extract(title, language="en-US"):
    r = requests.get(f'https://{language.split("-")[0]}.wikipedia.org/api/rest_v1/page/summary/{title}')
    return r.json()["extract"]

def get_related(text, language="en-US"):
  related_fields = []
  related_documents = []
  for annotation in wikify(text, language.split("-")[0]):
    related_fields.append(annotation)
    related_documents.append(get_wikipedia_extract(annotation, language))
  return related_fields, related_documents