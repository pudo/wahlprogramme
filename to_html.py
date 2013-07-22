from sections import load_platforms
from common import PARTIES, load_doc
from lxml import html
#from tfidf import load_idf_model, section_terms
from pprint import pprint
import json

TOPICS = json.load(open('data/topics.json'))
PARTIES = json.load(open('data/parties.json'))


def party_html(party, sections):
    doc = load_doc(party)
    next_section = 0
    section = None
    print [party, len(sections)]
    group = None

    doc.attrib['data-party'] = party
    doc.attrib['data-party-name'] = PARTIES[party]['name']
    doc.attrib['class'] = 'platform'

    for i, el in enumerate(doc.findall('./*')):
        assert el.tag != 'li'
        p = el.getparent()
        if (el.tag in ['h1', 'h2'] and sections[next_section].title == el.text) \
                or section is None:
            section = sections[next_section]
            group = html.Element('div')
            group.attrib['data-key'] = section.key
            group.attrib['data-title'] = section.title or 'Einleitung'
            group.attrib['data-topic'] = section.topic
            group.attrib['data-level'] = section.level or '1'
            group.attrib['data-topic-name'] = TOPICS[section.topic]['name']
            #group.attrib['data-topic-color'] = TOPICS[section.topic]['color']
            group.attrib['class'] = 'section'
            p.append(group)
            a = html.Element('a')
            a.attrib['name'] = section.key
            group.append(a)
            next_section += 1

        el.attrib['data-idx'] = str(i)
        p.remove(el)
        group.append(el)

    with open('data/html/%s.html' % party, 'wb') as fh:
        fh.write(html.tostring(doc))


if __name__ == '__main__':
    #model = load_idf_model()
    platforms = load_platforms()
    for party in PARTIES:
        party_html(party, platforms[party])
