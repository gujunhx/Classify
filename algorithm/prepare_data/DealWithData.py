import algorithm.resource
import os
import jieba
jieba.load_userdict('D:/program/news_category/algorithm/resource/external_dict.txt')

from algorithm.Traditional_Simple_transform import transform

import pickle

dic = {'other':'0.0','军情':'1.0', '社情':'2.0', '商情':'3.0', '政情':'4.0'}

stopword = []
def stopWords():
    fstop = open('D:/program/news_category/algorithm/resource/stopwords.txt', 'r', encoding='utf-8')
    for sw in fstop:
        stopword.append(sw.replace('\n',''))


def getPath(path):
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        label = dic.get(file_list[i])
        file_path = os.path.join(path, file_list[i])
        if os.path.isdir(file_path):
            getFile(label, file_path)



def getFile(label, path):
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        file_path = os.path.join(path, file_list[i])
        readFile(label, file_path)

def readFile(label, file):
    source_content = open(file,'r',encoding='utf-8').read()
    simple_content = transform.Traditional2Simplified(source_content)
    words = list(jieba.cut(simple_content))
    prepare(label, words)


def prepare(label, words):
    use_words = label+'  '
    for word in words:
        if word not in stopword and len(word) > 1 and check_contain_chinese(word):
            use_words += word + ','
    writeFile(use_words[:-1])

def isNum(word):
    return word.isdigit()

def check_contain_chinese(word):
    for ch in word:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def writeFile(data):
    data_file.write(data+'\n')



data_file = open('data.txt','a+')
stopWords()
data_path = 'C:/Users/isinonet/Desktop/category'
getPath(data_path)



