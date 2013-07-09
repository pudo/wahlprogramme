import math
from sections import load_platforms
from pprint import pprint
from collections import defaultdict


def load_values():
    values = {}
    with open('data/values.txt', 'rb') as fh:
        for line in fh:
            label, terms = line.split(':')
            terms = [t.strip() for t in terms.split(',')]
            for term in terms:
                values[term] = label
    pprint(values)
    return values

if __name__ == '__main__':
    #model = load_idf_model()
    values = load_values()
    platforms = load_platforms()
    scores = {}
    lengths = {}
    for party, sections in platforms.items():
        lengths[party] = sum([len(s) for s in sections])
        scores[party] = defaultdict(lambda: defaultdict(int))
        token_offset = 0
        for section in sections:
            for token in section.tokens:
                token_offset += 1
                label = values.get(token)
                if label is not None:
                    pct = math.floor((float(token_offset)/(lengths[party]+1))*100)
                    scores[party][label][int(pct)] += 1
        scores[party] = dict(scores[party])
    pprint(lengths)
    pprint(scores)
