from lxml import html
import re
from pdfclean import *

fh = open('html/linke.html', 'rb')
html_ = fh.read()
html_ = html_.replace('-<br/>', '')
html_ = html_.replace('&#160;', ' ')
doc = html.fromstring(html_)
fh.close()

NEWPAGE = 'NEWPAGE'
text = []
last_style = None

for el in doc.findall('.//body/div/*'):
    ecls = el.get('class') or ''
    if len(el.findall('.//i')):
        continue
    #print [ecls, ]
    eltext = el.text_content().strip()
    if ecls == 'ft00' or ecls == 'ft03' or el.tag == 'img':
        # or ecls == 'ft05':
        #text.append(NEWPAGE)
        continue
    #elif ecls == 'ft01' or el.tag == 'img':
    #    continue
    elif ecls == 'ft01':
        #eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n# ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif ecls == 'ft06' or ecls == 'ft04':
        btext = el.find('./b').text.strip()
        if len(btext) < 5 and btext.endswith(')'):
            text.append('\n' + eltext)
            continue
        #eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n## ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif el.tag == 'p':
        style = el.get('style', '')
        if 'left:369px' in style:
            eltext = '\n* ' + eltext
        elif 'left:94px' in style:
            eltext = '\n* ' + eltext
        elif 'left:73px' in style:
            eltext = '\n* ' + eltext
        elif check_paragraph(last_style, style, 30):
            eltext = '\n' + eltext
        last_style = style
        if eltext is not None:
            text.append(eltext)
        #text.append('')
        if el.tail is not None and len(el.tail.strip()):
            text.append(el.tail.strip())
    else:
        #pass
        print [el.tag, el.text, el.tail]

fh = open('markdown/linke.mdown', 'wb')
text = '\n'.join(text)

text = text.replace('\n\n\n', '\n')

while True:
    ntext = re.sub('# (.*)\n\n\n?# ', '# \g<1> ', text)
    if ntext == text:
        break
    text = ntext


while True:
    ntext = re.sub('## (.*)\n\n\n?## ', '## \g<1> ', text)
    if ntext == text:
        break
    text = ntext

text = text.replace('-\n', '')

#text = re.sub('# ([0-9]+.).\n\n# ', '# \g<1> ', text)
#text = text.replace('-\n\n# ', '')
text = re.sub('([^\n])\n([^\n])', '\g<1> \g<2>', text)

while '  ' in text:
    text = text.replace('  ', ' ')

fh.write(text.encode('utf-8'))
fh.close()
