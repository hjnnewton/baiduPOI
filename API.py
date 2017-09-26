# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals

from bosonnlp import BosonNLP

# 注意：在测试时请更换为您的API token
nlp = BosonNLP('Reg0KvHM.17970.YFwdM3sID8xa')
test = open("地标.txt")
try:
    correct = 0
    list_of_test = []
    for line in test.readlines()[100:104]:
        line = line.strip('\n')
        list_of_test.append(line)
    for entity in list_of_test:
        result = nlp.ner(entity)[0]
        words = result['word']
        entities = result['entity']
        for entity in entities:
            if entity[2] == 'location' or entity[2] == 'org_name' or entity[2] == 'company_name':
                correct = correct + 1
            else:
                print(''.join(words[entity[0]:entity[1]]), entity[2])
    precision = correct/len(list_of_test)
    print(correct, precision)
finally:
    test.close()
