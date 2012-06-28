# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
class Pinyin():

    def __init__(self, data_path='./Mandarin.dat'):
        self.dict = {}
        for line in open(data_path):
            k, v = line.split('\t')
            self.dict[k] = v
        self.splitter = ''

    def pinyin(self, chars):
        result = []
        for char in chars:
            key = "%X" % ord(char)
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1].lower())
            except:
                result.append(char)
        return self.splitter.join(result)

    def pinyin_first(self, chars):
        result = []
        for char in chars:
            key = "%X" % ord(char)
            try:
                pinyins = self.dict[key].split(" ")[0].strip()[:-1].lower()
                result.append(pinyins[0])
            except:
                result.append(char)
        return self.splitter.join(result)

