import re
import codecs
#词性标注，采用5倍交叉验证

def train(testOrder):
    '用语料库训练得到HMM的参数：转移概率，输出概率，初始状态分布...参数testOrder为用作测试的文本序号'
    InitialStateDict = dict()   #存储初始状态分布的词典，key=词性，value=频次
    TransitionDict = dict()     #存储词性转移频次的词典，key=词性，value也是一个dict：key=下一个词性，value=频次
    ObservationDict = dict()    #存储词性->观察词汇的输出频次的词典，key=词性，value也是一个dict：key=单词，value=频次
    for i in range(1,6,1):#循环1-5各训练文本，用testOrder以外的4各文本训练
        if i != testOrder:
            trainFileName = 'train{}.txt'
            trainFileName = trainFileName.format(str(i))
            with codecs.open(trainFileName,'r','UTF-8'):

    return

#main program
train(5)