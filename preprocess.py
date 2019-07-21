import collections
def preprocess(filename):
    sentence_with_tag = []
    words = set()
    tags = set()
    with open(filename, 'r') as file_:
        while True:
            line = file_.readline()
            if line.startswith('b100-'):
                sentence_with_tag.append(collections.OrderedDict())
                while True:
                    line = file_.readline()
                    if line is '\n' or '':
                        break
                    split = line.split('\t')
                    sentence_with_tag[-1][split[0].lower()] = split[1][:-1]
                    words.add(split[0].lower())
                    tags.add(split[1][:-1])
            else:
                break
    return sentence_with_tag, words, tags
