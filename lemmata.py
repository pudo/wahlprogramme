from collections import defaultdict
import re

LINEFMT = re.compile(r'(.*)\|([NVA])\t\[(.*)\]')


def load_lemmata():
    print "Loading all the words..."
    values = defaultdict(list)
    with open('data/lemmata.txt', 'rb') as fh:
        for line in fh:
            match = LINEFMT.match(line)
            word, pos, forms = match.groups()
            values[word].append((word, pos))
            for form in forms.split(','):
                values[form].append((word, pos))
    return values

LEMMATA = load_lemmata()


def is_type(word, type_):
    for lemma, pos in LEMMATA.get(word, []):
        if pos == type_:
            return True
    return False

if __name__ == '__main__':
    print len(LEMMATA)
