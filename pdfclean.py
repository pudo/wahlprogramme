import re


def clean_spacing(text):
    while True:
        ntext = re.sub('# (.*)\n+# ', '# \g<1> ', text)
        if ntext == text:
            break
        text = ntext

    while True:
        ntext = re.sub('## (.*)\n+## ', '## \g<1> ', text)
        if ntext == text:
            break
        text = ntext

    text = re.sub('([^\n])\n([^\n])', '\g<1> \g<2>', text)

    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def check_paragraph(last, cur, min):
    if last is None:
        return False
    last = dict([l.split(':') for l in last.split(';')])
    cur = dict([l.split(':') for l in cur.split(';')])
    last_top = int(last.get('top', '').replace('px', ''))
    cur_top = int(cur.get('top', '').replace('px', ''))
    diff = cur_top - last_top
    if diff > min:
        return True
    return False
    print [last_top, cur_top, cur_top - last_top]

