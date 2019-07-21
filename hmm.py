import collections
import copy
import pdb

class HMMModel:
    def __init__(self, sentence_with_tag, words, tags):
        self.sentence_with_tag = copy.deepcopy(sentence_with_tag)
        self.words = words
        self.tags = tags
        self.num_of_sen = len(sentence_with_tag)
        # tag to tag
        self.A = {}
        # tag to word
        self.B = {}
        # initial tag
        self.Pi = {}
        self.path = []

    def get_model_params(self):
        for i in self.tags:
            self.Pi[i] = 1
            self.A[i] = {}
            self.B[i] = {}
            for j in self.tags:
                self.A[i][j] = 1
            for j in self.words:
                self.B[i][j] = 1

        for i in self.sentence_with_tag:
            word_with_tag = i.popitem(last=False)
            self.Pi[word_with_tag[1]] += 1
            self.B[word_with_tag[1]][word_with_tag[0]] += 1
            length = len(i)
            for k in range(length):
                next_word_with_tag = i.popitem(last=False)
                self.A[word_with_tag[1]][next_word_with_tag[1]] += 1
                self.B[next_word_with_tag[1]][next_word_with_tag[0]] += 1
                word_with_tag = next_word_with_tag

        A_r = {}
        B_r = {}
        temp_A = copy.deepcopy(self.A)
        temp_B = copy.deepcopy(self.B)
        for i in self.tags:
            self.Pi[i] = self.Pi[i] / (self.num_of_sen + len(self.tags))
            A_r[i] = sum([j for j in self.A[i].values()])
            B_r[i] = sum([j for j in self.B[i].values()])
        for i in self.tags:
            for j in self.tags:
                self.A[i][j] = temp_A[i][j] / A_r[i]
            for j in self.words:
                self.B[i][j] = temp_B[i][j] / B_r[i]
    def _find_max(self, delta, tag):
        li = [[i, self.A[i][tag] * delta[i]]  for i in self.A.keys()]
        ind = None
        value = -1
        for i in li:
            if i[1] > value:
                value = i[1]
                ind = i[0]
        return value, ind

    def viterbi(self, sentence):
        # sentence should be a list of words which form a sentence
        for i in range(len(sentence)):
            sentence[i] = sentence[i].lower()
        
        delta = []
        phi = []
        
        delta.append(collections.OrderedDict())
        phi.append(collections.OrderedDict())
        for j in self.tags:
            delta[-1][j] = self.Pi[j] * self.B[j][sentence[0]]
            phi[-1][j] = 0

        num_of_word = len(sentence)
        for i in range(num_of_word - 1):
            delta.append(collections.OrderedDict())
            phi.append(collections.OrderedDict())
            next_word = sentence[i + 1]
            for j in self.tags:
                value, ind = self._find_max(delta[-2], j)
                delta[-1][j] = value * self.B[j][next_word]            
                phi[-1][j] = ind
        
        tag_res = []
        P_max = -1
        Ind = -1
        for i in delta[-1].items():
            if i[1] > P_max:
                P_max = i[1]
                Ind = i[0]
        last = Ind
        for i in reversed(phi):
            tag_res.append(i[Ind])
            Ind = i[Ind]
        tag_res.pop()
        tag_res = list(reversed(tag_res))
        tag_res.append(last)
        return tag_res
