from lxml import html
import re

fh = open('html/cdu.html', 'rb')
html_ = fh.read()
html_ = html_.replace('-<br/>', '')
html_ = html_.replace('&#160;', ' ')
doc = html.fromstring(html_)
fh.close()

NEWPAGE = 'NEWPAGE'
text = []

for el in doc.find('.//body').getchildren():
    if el.tag == 'a':
        text.append(NEWPAGE)
    elif el.tag == 'b':
        if el.text and len(el.text.strip()):
            text.append('\n\n# ' + el.text + '\n')
        if el.tail is not None:
            text.append(el.tail.strip())
    elif el.tag == 'br':
        if el.text is not None:
            text.append(el.text.strip())
        text.append('')
        if el.tail is not None:
            text.append(el.tail.strip())
    else:
        pass
        #print [el.tag, el.text, el.tail]

fh = open('markdown/cdu.mdown', 'wb')
text = '\n'.join(text)
text = text.replace('\n\n', '\n')
text = text.replace('\n\n' + NEWPAGE + '\n\n', '')
text = re.sub('(### .*)\n+### ', '\g<1> ', text)
text = re.sub('(## .*)\n+## ', '\g<1> ', text)
text = re.sub('(# .*)\n+# ', '\g<1> ', text)
text = text.replace('-\n\n# ', '')
text = text.replace(NEWPAGE, '')
text = re.sub('([^\n])\n([^\n])', '\g<1> \g<2>', text)

texts = []
for line in text.split('\n'):
    if re.match('# \d+. .*', line):
        pass
    elif re.match('# \d+.\d+. .*', line):
        line = '#' + line
    elif re.match('# .*', line):
        line = '##' + line
    texts.append(line)
text = '\n'.join(texts)

while '  ' in text:
    text = text.replace('  ', ' ')

fh.write(text.encode('utf-8'))
fh.close()
