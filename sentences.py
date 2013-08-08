import re
import dataset
import hashlib
from sections import load_platforms
from collections import defaultdict
from text import normalize, tokenize
from pprint import pprint
import json

engine = dataset.connect('sqlite:///sentences.db')
table = engine['sentences']

SENTENCE = re.compile(r'[\.!?]\s+', re.M)
CLEANUP = re.compile(r'\s+', re.M)
EXCEPTIONS = map(re.compile, ['Mio$', 'Mrd?$', 'Art$', '\sz$', 'z\. ?B$', '\sd$', 'd\. ?h$', '\su$', 'u. ?a$', 'bzw$', '\d+$', ' sog'])
FORMATTING = re.compile('^(\s?[\#\*]+)?\s*([IVX0-9]{1,2}\.[IVX0-9]{0,2}\.?\s)?\s*(.*)')

def sentences(section):
    sens = []
    for s in SENTENCE.split(section.text):
        s = s.strip()
        s = CLEANUP.sub(' ', s)
        m = FORMATTING.match(s)
        if m is not None:
            s = m.groups()[2]
        done = False
        for exc in EXCEPTIONS:
            if len(sens) and exc.search(sens[-1]):
                sens[-1] += '. ' + s
                done = True
                break
        if not done:
            sens.append(s)
    
    #pprint(sens)
    return sens

def check_valid(sentence):
    if len(sentence.split()) < 3 or len(sentence.strip()) < 10:
        return False
    if sentence[0] != sentence[0].upper():
        return False
    return True

def split_sentences():
    platforms = load_platforms()
    lengths = defaultdict(list)
    for party, sections in platforms.items():
        for section in sections:
            for i, sentence in enumerate(sentences(section)):
                lengths[party].append(len(sentence.split()))
                data = {
                    'num': i,
                    'hash': hashlib.sha1(sentence.encode('ascii', 'replace')).hexdigest(),
                    'text': sentence,
                    'party': party,
                    'section': section.key
                }
                #if not check_valid(sentence):
                data['valid'] = check_valid(sentence)
                table.upsert(data, ['num', 'section'])

    for party, sens in lengths.items():
        avg = sum(sens) / len(sens)
        print 'PARTY', party, 'AVG', avg

if __name__ == '__main__':
    split_sentences()

