import math
import json
from collections import defaultdict
from sections import load_platforms

ALL = 'global'


def generate_idf_model():
    terms = {
        ALL: defaultdict(int)
    }

    print "Extracting..."
    counts = {
        ALL: 0
    }

    for party, sections in load_platforms().items():
        counts[party] = 0
        terms[party] = defaultdict(int)

        for section in sections:
            counts[party] += 1
            counts[ALL] += 1

            for token in section.tokens:
                terms[party][token] += 1
                terms[ALL][token] += 1

    print "Calculating IDF..."
    data = {}
    for party, tokens in terms.items():
        num = float(counts[party])
        data[party] = {}

        for term, count in tokens.items():
            idf = math.log((num/(1+count)))
            data[party][term] = idf

    with open('data/idf.json', 'wb') as fh:
        json.dump(data, fh)


def load_idf_model():
    with open('data/idf.json', 'rb') as fh:
        return json.load(fh)


def section_terms(model, section, base=ALL):
    terms = defaultdict(int)
    for token in section.tokens:
        terms[token] += 1

    total = float(sum(terms.values()))
    if total == 0:
        return []
    max_f = max(terms.values())/total
    #print "MAX", max_f, max(terms.values()), terms.values()
    tf_idfs = {}
    for term, count in terms.items():
        if count < 2:
            continue
        tf = 0.5 + ((0.5*(count/total))/max_f)
        tf_idfs[term] = tf * model[base].get(term, 0)

    return sorted(tf_idfs.items(), key=lambda (a, b): b, reverse=True)


if __name__ == '__main__':
    generate_idf_model()
