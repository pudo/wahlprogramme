from sections import load_platforms
from collections import defaultdict
from text import normalize, tokenize
from pprint import pprint
import json


def norm(text):
    text = text.decode('utf-8')
    return normalize(text)


def classify():
    decisive = map(norm, open('decisive.txt', 'rb').readlines())
    loriot = list(tokenize(open('loriot.txt', 'rb').read().decode('utf-8')))
    #print decisive
    #return
    platforms = load_platforms()
    scores = defaultdict(dict)
    for party, sections in platforms.items():
        for section in sections:
            scores[party][section.key] = {'tokens': len(section)}
            text = normalize(section.text)
            n_decisive = 0.0
            for phrase in decisive:
                if phrase in text:
                    n_decisive += 1
            scores[party][section.key]['decisive'] = n_decisive/len(section)
            n_loriot = 0.0
            for token in loriot:
                if token in text:
                    n_loriot += 1
            scores[party][section.key]['loriot'] = n_loriot/len(section)
            #terms = section_terms(model, section)
            #terms = [(t, s) for t, s in terms]
            #print [party, section.title, [t for t, s in terms[:10]]]
    #pprint(scores)
    with open('data/language.json', 'wb') as fh:
        json.dump(dict(scores), fh, indent=2)


if __name__ == '__main__':
    classify()
