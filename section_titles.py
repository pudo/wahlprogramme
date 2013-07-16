import re
import json
from sections import load_platforms

prefix = re.compile(r'[iIvVX0-9]+.?([iIvV0-9]+.?)? (.*)')

if __name__ == '__main__':
    platforms = load_platforms()
    titles = {}
    lengths = {}
    for party, sections in platforms.items():
        titles[party] = []
        lengths[party] = sum([len(s) for s in sections])
        for section in sections:
            short_title = section.title
            match = prefix.match(section.title or '')
            if match is not None:
                #print [section.title, match.groups()]
                short_title = match.groups()[-1]
            #else:
            #    print [section.title]
            titles[party].append({
                'title': section.title or 'Unbenannt',
                'short_title': short_title or 'Unbenannt',
                'tokens': len(section),
                'total': lengths[party],
                'topic': section.topic,
                'key': section.key
            })

    with open('data/sections_titles.json', 'wb') as fh:
        json.dump(titles, fh)
