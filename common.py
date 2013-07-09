#import dataset
from lxml import html
from markdown import markdown

PARTIES = ['fdp', 'cdu', 'gruene', 'spd', 'linke']


#engine = dataset.connect('sqlite:///programme.sqlite3')
#titles = engine.get_table('titles')


def load_file(party):
    with open('markdown/%s.mdown' % party, 'rb') as fh:
        return markdown(fh.read().decode('utf-8'))


def load_doc(party):
    html_ = load_file(party)
    return html.fromstring(html_)
