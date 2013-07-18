from sections import load_platforms
from tfidf import load_idf_model, section_terms
from pprint import pprint


if __name__ == '__main__':
    model = load_idf_model()
    platforms = load_platforms()
    for party, sections in platforms.items():
        for section in sections:
            terms = section_terms(model, section)
            terms = [(t, s) for t, s in terms]
            print [party, section.title, [t for t, s in terms[:10]]]
