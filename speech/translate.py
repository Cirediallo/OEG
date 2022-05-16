import os
from google.cloud import translate

def translate_text(text, source="en-US", target="fr-FR", project_id="speechtotextapi-340414"):

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent= parent,
        contents= [text],
        mime_type= "text/plain",  # mime types: text/plain, text/html
        source_language_code= source,
        target_language_code= target,
    )
    
    return response.translations[0].translated_text
    """print(response.translations[0].translated_text)
    fhand = open(f"translated_{target}.txt", "a", encoding="utf-8")
    for translation in response.translations:
        fhand.write(" " + translation.translated_text)
    fhand.close()"""
    
print(translate_text("Hello there", source="en-US", target="ar-SA"))