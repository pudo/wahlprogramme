from lxml import html
import re
from pdfclean import *

fh = open('html/spd.html', 'rb')
html_ = fh.read()
html_ = html_.replace('-<br/>', '')
html_ = html_.replace('&#160;', ' ')
doc = html.fromstring(html_)
fh.close()

text = []
last_style = None

for el in doc.findall('.//body/div/*'):
    ecls = el.get('class') or ''
    #print [ecls, ]
    eltext = el.text_content()
    if ecls == 'ft00' or ecls == 'ft01' or el.tag == 'img' or ecls == 'ft08':
        continue
    elif ecls == 'ft02':
        eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n# ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif ecls == 'ft07':
        eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n## ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif el.tag == 'p':
        style = el.get('style', '')
        if 'left:74px' in style:
            eltext = '\n* ' + eltext
        elif check_paragraph(last_style, style, 30):
            eltext = '\n' + eltext
        last_style = style
        if eltext is not None:
            text.append(eltext)
        text.append('')
        if el.tail is not None:
            text.append(el.tail.strip())
    else:
        #pass
        print [el.tag, el.text, el.tail]

text = '\n'.join(text)

text = text.replace('\n\n\n', '\n')
text = text.replace('-\n', '')

text = clean_spacing(text)

fh = open('markdown/spd.mdown', 'wb')
fh.write(text.encode('utf-8'))
fh.close()
