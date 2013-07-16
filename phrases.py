from sections import load_platforms
from tfidf import load_idf_model, section_terms
from lemmata import is_type
from pprint import pprint


if __name__ == '__main__':
    #model = load_idf_model()
    platforms = load_platforms()
    for party, sections in platforms.items():
        for section in sections:
            adj = None
            for token in section.tokens:
                if adj is not None and is_type(token, 'N'):
                    print [adj + ' ' + token]
                    adj = None
                elif is_type(token, 'A'):
                    adj = token
                else:
                    adj = None
            #terms = section_terms(model, section)
            #print [party, section.title, [t for t, s in terms[:10]]]
