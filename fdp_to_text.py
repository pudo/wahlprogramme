from lxml import html
import re
from pdfclean import *

fh = open('html/fdp.html', 'rb')
html_ = fh.read()
html_ = html_.replace('-<br/>', '')
html_ = html_.replace('<br/>&#160;<br/>', '\n\n')

html_ = html_.replace('&#160;', ' ')
doc = html.fromstring(html_)
fh.close()

NEWPAGE = 'NEWPAGE'
text = []
last_style = None

for el in doc.findall('.//body/div/*'):
    ecls = el.get('class') or ''
    #print [ecls, ]
    eltext = el.text_content().strip()
    if ecls == 'ft00':
        #text.append(NEWPAGE)
        continue
    elif ecls == 'ft01' or el.tag == 'img':
        continue
    elif ecls == 'ft02':
        #eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n# ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif ecls == 'ft06':
        #eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n## ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif el.tag == 'p':
        style = el.get('style', '')
        if 'left:81px' in style:
            eltext = '* ' + eltext
        #elif check_paragraph(last_style, style, 30):
        #    eltext = '\n' + eltext
        if eltext is not None:
            text.append(eltext.strip())
        text.append('')
        if el.tail is not None:
            text.append(el.tail.strip())
    else:
        #pass
        print [el.tag, el.text, el.tail]

fh = open('markdown/fdp.mdown', 'wb')
text = '\n'.join(text)

text = text.replace('\n\n\n', '\n')
text = text.replace('\n' + NEWPAGE + '\n', '')
text = text.replace('-\n', '')

while True:
    ntext = re.sub('# (.*)\n\n\n# ', '# \g<1> ', text)
    if ntext == text:
        break
    text = ntext

while True:
    ntext = re.sub('## (.*)\n\n\n## ', '## \g<1> ', text)
    if ntext == text:
        break
    text = ntext
#text = re.sub('# ([0-9]+.).\n\n# ', '# \g<1> ', text)
#text = text.replace('-\n\n# ', '')
text = text.replace(NEWPAGE, '')
text = re.sub('([^\n])\n([^\n])', '\g<1> \g<2>', text)

while '  ' in text:
    text = text.replace('  ', ' ')

#texts = []
#for line in text.split('\n'):
#    if re.match('# \d+. .*', line):
#        pass
#    elif re.match('# \d+.\d+. .*', line):
#        line = '#' + line
#    elif re.match('# .*', line):
#        line = '##' + line
#    texts.append(line)
#text = '\n'.join(texts)

fh.write(text.encode('utf-8'))
fh.close()
