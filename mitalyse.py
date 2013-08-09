import math
import json
from sections import load_platforms
from pprint import pprint
from collections import defaultdict


def load_values():
    values = {}
    with open('data/values.txt', 'rb') as fh:
        for line in fh:
            if line.strip().startswith('#'):
                continue
            label, terms = line.split(':')
            terms = [t.strip() for t in terms.split(',')]
            for term in terms:
                values[term] = label
    pprint(values)
    return values

if __name__ == '__main__':
    #model = load_idf_model()
    values = ['gerecht*', '*gerechtigkeit*', 'chancen*']
    platforms = load_platforms()
    lengths = {}
    scores = defaultdict(lambda: defaultdict(int))
    for party, sections in platforms.items():
        lengths[party] = sum([len(s) for s in sections])
        token_offset = 0
        for section in sections:
            for token in section.tokens:
                for value in values:
                    vr = value.replace('*', '')
                    if value.endswith('*') and token.startswith(vr):
                        scores[party][value] += 1
                    elif value.startswith('*') and token.endswith(vr):
                        scores[party][value] += 1
                    elif vr == token:
                        scores[party][value] += 1
        scores[party] = dict(scores[party])
    #pprint(lengths)
    data = {
        'lengths': lengths,
        'scores': dict(scores)
    }
    pprint(data)
