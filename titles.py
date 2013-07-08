from load import PARTIES, load_doc


def all_titles():
    for party in PARTIES:
        doc = load_doc(party)

        for h in doc.findall('.//*'):
            if not h.tag in ['h1', 'h2']:
                continue
            print [party, h.tag, h.text]

all_titles()