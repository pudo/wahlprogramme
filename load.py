from lxml import html
import markdown

PARTIES = ['fdp', 'cdu', 'gruene', 'spd', 'linke']


def load_file(party):
    with open('markdown/%s.mdown' % party, 'rb') as fh:
        html = markdown.markdown(fh.read().decode('utf-8'))
        return html


def load_doc(party):
    html_ = load_file(party)
    return html.fromstring(html_)
