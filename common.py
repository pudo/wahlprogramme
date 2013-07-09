import os
#import dataset
from lxml import html
from markdown import markdown
from nomenklatura import Dataset

PARTIES = ['fdp', 'cdu', 'gruene', 'spd', 'linke']

nomenklatura = Dataset('btw13-titles',
                       api_key=os.environ.get('NOMENKLATURA_API_KEY'))

#engine = dataset.connect('sqlite:///programme.sqlite3')
#titles = engine.get_table('titles')


def load_file(party):
    with open('markdown/%s.mdown' % party, 'rb') as fh:
        return markdown(fh.read().decode('utf-8'))


def load_doc(party):
    html_ = load_file(party)
    return html.fromstring(html_)
