from sections import load_platforms
from collections import defaultdict
from pprint import pprint
import json

SKIP_TOPIC = 'intro'


if __name__ == '__main__':
    result = {}
    data = load_platforms()
    for party, sections in data.items():
        total_tokens = sum([len(s.tokens) for s in sections if s.topic != SKIP_TOPIC])
        topics = defaultdict(float)
        for section in sections:
            if section.topic == SKIP_TOPIC:
                continue
            #print [section.topic, section.title]
            #print [len(section.tokens), (len(section.tokens)/float(total_tokens))*100]
            topics[section.topic] += (len(section.tokens)/float(total_tokens)) * 100
        pprint(dict(topics))
        print "TOTAL", sum(topics.values())
        result[party] = dict(topics)
    with open('data/topic_shares.json', 'wb') as fh:
        json.dump(result, fh)
