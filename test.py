from pattern.de import parse, split
from sections import load_platforms
from pprint import pprint


def test():
    platforms = load_platforms()
    for party, sections in platforms.items():
        for section in sections:
            tagged = split(parse(section.text))
            for sentence in tagged:
                #if not sentence.is_question:
                #    continue
                try:
#                    for word in sentence.words:
#                        print word.tags #dir(word)
                    #print [sentence.subjects, sentence.verbs]
                    #print [sentence.is_question]
                    #print [sentence.words]
                    print [sentence.text]
                except UnicodeEncodeError:
                    pass
            #print dir(s)
            #return

if __name__ == '__main__':
    test()
