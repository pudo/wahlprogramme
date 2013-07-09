from common import PARTIES, load_doc, nomenklatura


def all_titles():
    for party in PARTIES:
        doc = load_doc(party)

        for i, h in enumerate(doc.findall('.//*')):
            if not h.tag in ['h1', 'h2']:
                continue
            #titles.upsert({
            #    'party': party,
            #    'index': i,
            #    'element': h.tag,
            #    'text': h.text
            #}, ['party', 'text'])
            print [party, h.tag, h.text]
            fp = '[%s:%s] %s' % (party, h.tag, h.text)
            try:
                entity = nomenklatura.lookup(fp)
                print [h.text, entity.name]
            except Exception, e:
                print e


if __name__ == '__main__':
    all_titles()
