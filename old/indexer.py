import os
import requests
import json
from sections import load_platforms
from pprint import pprint

URL = 'https://api.swiftype.com/api/v1/engines/wahlprogramme/document_types/section/documents.json'
auth_token = os.environ.get('SWIFTYPE_AUTH_TOKEN')

if __name__ == '__main__':
    platforms = load_platforms()
    for party, sections in platforms.items():
        for section in sections:
            data = {
                "auth_token": auth_token,
                "document": {
                    "external_id": section.key,
                    "fields": [
                        {"name": "title", "value": section.title, "type": "string"},
                        {"name": "topic", "value": section.topic, "type": "enum"},
                        {"name": "party", "value": party, "type": "enum"},
                        {"name": "text", "value": section.text, "type": "text"},
                        {"name": "level", "value": section.level, "type": "integer"},
                    ]
                }
            }
            #pprint(data)
            data = json.dumps(data)
            res = requests.post(URL, headers={'Content-Type': 'application/json'}, data=data)
            print res.status_code, res.content
            #terms = section_terms(model, section)
            #terms = [(t, s) for t, s in terms]
            #print [party, section.title, [t for t, s in terms[:10]]]
