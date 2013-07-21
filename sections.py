import os
import re
import json
from lxml import html
from hashlib import sha1
from common import PARTIES, load_doc
from text import tokenize
from nomenklatura import Dataset


class Section(object):

    def __init__(self, party):
        self.party = party
        self.texts = []
        self.elem = html.Element("div")
        self.title = None
        self.level = "1"
        self.topic = 'intro'

    @property
    def text(self):
        text = '\n'.join([t for t in self.texts if t])
        return text.strip()

    @property
    def valid(self):
        return len(self.text) > 0

    @property
    def tokens(self):
        if not hasattr(self, '_tokens'):
            self._tokens = list(tokenize(self.text))
        return self._tokens

    @property
    def key(self):
        text = self.party + (self.title or 'Unbenannt')
        return sha1(text.encode('ascii', 'ignore')).hexdigest()[:7]

    @property
    def sentences(self):
        #return re.split(r'([\S])+\.\s', self.text)
        _s = []
        for sentence in self.text.split('.'):
            sentence = sentence.strip()
            if len(sentence):
                _s.append(sentence)
        return _s

    def to_json(self):
        return {
            'party': self.party,
            'texts': self.texts,
            'title': self.title,
            'level': self.level,
            'topic': self.topic,
            'key': self.key
        }

    def __len__(self):
        return len(self.tokens)

    @classmethod
    def from_json(cls, d):
        obj = cls(d['party'])
        obj.texts = d['texts']
        obj.title = d['title']
        obj.level = d['level']
        obj.topic = d['topic']
        return obj

    def __repr__(self):
        return u'<Section(%s,%s,%s)>' % (self.party, self.topic, self.title)


def extract_sections(party):
    doc = load_doc(party)

    nomenklatura = Dataset('btw13-titles',
                           api_key=os.environ.get('NOMENKLATURA_API_KEY'))

    current = Section(party)
    for i, h in enumerate(doc.findall('.//*')):
        if h.tag in ['h1', 'h2']:
            if current.valid:
                yield current
            current = Section(party)
            current.title = h.text
            current.level = h.tag[1:]
            fp = '[%s:%s] %s' % (party, h.tag, h.text)
            try:
                entity = nomenklatura.lookup(fp)
                current.topic = entity.name
            except Exception, e:
                print [fp]
                print e
        #if h.getparent() == doc:
        #    #print "XXX", h
        current.texts.append(h.text)
    if current.valid:
        yield current


def load_platforms():
    print "Loading serialized platforms..."
    sections = {}
    with open('data/sections.json', 'rb') as fh:
        data = json.load(fh)
        for party in PARTIES:
            sections[party] = []
            for sect in data.get(party, []):
                sections[party].append(Section.from_json(sect))
        return sections



if __name__ == '__main__':
    data = {}
    sections = {}
    for party in PARTIES:
        data[party] = []
        sections[party] = []
        for section in extract_sections(party):
            print [section.party, section.topic, section.title, str(len(section.tokens))     + ' Worte']
            data[party].append(section.to_json())
            sections[party].append(section)
    with open('data/sections.json', 'wb') as fh:
        json.dump(data, fh)
