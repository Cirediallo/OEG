import os
from google.cloud import translate

def translate_text(text, lang_source, lang_target, project_id):

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent= parent,
        contents= [text],
        mime_type= "text/plain",  # mime types: text/plain, text/html
        source_language_code= lang_source,
        target_language_code= lang_target,
    )
    
    return response.translations[0].translated_text