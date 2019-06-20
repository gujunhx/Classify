import jieba
from algorithm.Traditional_Simple_transform import transform
import pickle

stopword = []
def stopWords():
    fstop = open('../resource/stopwords.txt', 'r', encoding='utf-8')
    for sw in fstop:
        stopword.append(sw.replace('\n',''))

def check_contain_chinese(word):
    for ch in word:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def getContent(content):
    test = []
    use_words = ''
    simple_content = transform.Traditional2Simplified(content)
    words = list(jieba.cut(simple_content))
    for word in words:
        if word not in stopword and len(word) > 1 and check_contain_chinese(word):
            use_words += word + ','
    loadModel = pickle.load(open('../model/NB.model', 'rb'))
    test.append(use_words[:-1])
    pre = loadModel.predict(test)
    print(pre)

stopWords()
content = '2016 年，也就是两年前，7月24日，当 Alban 在博客发布文章，埋怨 Transpyrenea 不值得参加时，他肯定不会想到，两年后，竟有一群从全世界各个角落出发，朝法国西班牙边境附近小城 Banyuls sur Mer 前进的疯子，是为了他口中这不值得参加的比赛而来。'
getContent(content)