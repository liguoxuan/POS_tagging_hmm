from hmm import HMMModel
from preprocess import preprocess

import argparse
import numpy as np 
import pdb

def precision(test_set, model):
    ri, fal = 0, 0
    for i in test_set:
        input_, ans = [], []
        for k in i:
            input_.append(k)
            ans.append(i[k])
        res = model.viterbi(input_)

        for j in range(len(ans)):
            if res[j] == ans[j]: 
                ri += 1
            else:
                fal += 1
    return (ri / (ri + fal))

def test(filename):
    sentence_with_tag, words, tags = preprocess(args.filename)
    content = len(sentence_with_tag)
    ind = np.random.permutation(content)
    test_ind = ind[:int(0.1 * content)]
    train_ind = ind[int(0.1 * content):]
    test_set = []
    train_set = []
    for i in test_ind:
        test_set.append(sentence_with_tag[i])
    for i in train_ind:
        train_set.append(sentence_with_tag[i])
    model = HMMModel(train_set, words, tags)
    model.get_model_params()
    return precision(test_set, model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hmm model for pos tagging')
    parser.add_argument('--filename', default='brown-universal.txt')
    parser.add_argument('--times', default=10)
    args = parser.parse_args()
    times = args.times
    res = []
    
    for i in range(times):
        res.append(test(args.filename))
    print('{} times tests, results: '.format(times))
    print('--------------------------------')
    for i in range(times):
        print('Test {}, Precision & Recall: {}'.format(i + 1, res[i]))
    print('--------------------------------')
    print('Average Precision & Recall: {}'.format(sum(res) / times))
