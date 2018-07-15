#!python2
# coding: utf-8

import re
import nltk.stem
import math
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer


def process_text(line):
    split_symbol = r"[ ;,:.\s\"]"
    line = line.lower()
    tokens = re.split(split_symbol, line)
    cleanTokens = []
    # 提取词干 词根还原
    stemmer = nltk.stem.SnowballStemmer('english')
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for token in tokens:
        if token.isalpha():
            token = stemmer.stem(lemmatizer.lemmatize(token))
        else:
            match = re.findall(r'[^a-z0-9]+', token)
            for i in match:
                # 只要英文单词与数字，删掉其他字符
                token = token.replace(i, '')
            if token.isalpha():
                token = stemmer.stem(lemmatizer.lemmatize(token))
        if len(token) > 1:
            cleanTokens.append(token)

    newline = ' '.join(cleanTokens)
    return newline


def similarity(vec1, vec2):
    multi = 0
    sum1 = 0
    sum2 = 0
    for i in range(len(vec1)):
        multi += vec1[i] * vec2[i]
        sum1 += math.pow(vec1[i], 2)
        sum2 += math.pow(vec2[i], 2)

    return multi / math.sqrt(sum1 * sum2)


def state(score):
    score = float(score)
    s = ''
    if score <= 0:
        s = "差"
    elif 0 < score <= 0.25:
        s = "一般"
    elif 0.25 < score <= 0.6:
        s = "较好"
    elif 0.6 < score:
        s = "好"

    return "    程度: " + s


def averageScore(vec):
    # 对本python文件而言，相对路径从当前文件夹开始，对web而言，相对路径从pyWeb_test开始
    all_vecs = np.loadtxt('/home/jw/PycharmProjects/sap_project/pyWeb_test/feature_vectors.txt').tolist()
    score_sum = 0

    for v in all_vecs:
        if v.count(0) == len(v):
            continue
        score_sum += similarity(vec, v)

    return str(score_sum / len(all_vecs))


def featureExtraction(text):
    document = []
    document.append(text)
    vector = HashingVectorizer(n_features=100)
    res = vector.transform(document).todense()
    return res


def mainProcess(text):
    text = process_text(text)
    vector = featureExtraction(text)
    vector = (vector[0].tolist())[0]
    if vector.count(0) == len(vector):
        return -1

    avgS = averageScore(vector)
    s = state(avgS)
    return avgS


print mainProcess("hello, there is a problem in the sap system, and I can't fixe it, can you help me? thank you very much!hello, there is a problem in the sap system, and I can't fixe it, can you help me? thank you very much!hello, there is a problem in the sap system, and I can't fixe it, can you help me? thank you very much! hahahaha")
