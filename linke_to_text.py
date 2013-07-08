from lxml import html
import re

fh = open('html/linke.html', 'rb')
html_ = fh.read()
html_ = html_.replace('-<br/>', '')
html_ = html_.replace('&#160;', ' ')
doc = html.fromstring(html_)
fh.close()

NEWPAGE = 'NEWPAGE'
text = []

for el in doc.findall('.//body/div/*'):
    ecls = el.get('class') or ''
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
    elif ecls == 'ft06':
        #eltext = eltext.upper().strip()
        if eltext and len(eltext.strip()):
            text.append('\n## ' + eltext + '\n\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif el.tag == 'p':
        if 'left:369px' in el.get('style', ''):
            eltext = '\n* ' + eltext
        if 'left:94px' in el.get('style', ''):
            eltext = '\n* ' + eltext
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
text = re.sub('([^\n])\n([^\n])', '\g<1> \g<2>', text)


fh.write(text.encode('utf-8'))
fh.close()
