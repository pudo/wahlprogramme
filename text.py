from unicodedata import normalize as ucnorm, category
import os


def normalize(text):
    if not isinstance(text, unicode):
        text = unicode(text)
    text = text.lower()
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if char == "'":
            continue
        if cat.startswith('C'):
            filtered.append(' ')
        elif cat.startswith('M'):
            # marks, such as umlauts
            #continue
            filtered.append(char)
        elif cat.startswith('Z'):
            # newlines, non-breaking etc.
            filtered.append(' ')
        elif cat.startswith('S'):
            # symbols, such as currency
            continue
        elif cat.startswith('L') or cat.startswith('N'):
            filtered.append(char)
        else:
        #    print (cat, char)
            filtered.append(' ')
    text = u''.join(filtered)
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return ucnorm('NFKC', text)


STOPFILE = os.path.join(os.path.dirname(__file__), 'stopwords.de.txt')
STOPWORDS = normalize(open(STOPFILE).read().decode('utf-8')).split()


def tokens_to_bigrams(tokens):
    last_token = None
    for token in tokens:
        if last_token is not None:
            yield '%s_%s' % (last_token, token)
        last_token = token


def tokenize(text):
    for token in normalize(text).split(' '):
        if not len(token) or token in STOPWORDS:
            continue
        yield token


def make_bigrams(text):
    tokens = tokenize(text)
    bigrams = tokens_to_bigrams(tokens)
    return bigrams


if __name__ == '__main__':
    print make_bigrams('Ich bin also eine Banane!')
