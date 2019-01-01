import re
import codecs
import math

def uni_init():
    '求训练预料中各词汇出现的频率以及词汇总量'
    #将训练文本"train.txt"中的 词&频次 存储到trainDict中
    trainDict = dict()           #key为单词，value为频次
    totalTrainWordsCnt = 0       #训练文本中词总数
    trainDict['<BOS>'] = 0
    trainDict['<EOS>'] = 0
    with codecs.open('train.txt','r','UTF-8') as trainFile:
        lines = trainFile.readlines()
        for i in range(0,lines.__len__(),1):    #取出每行单词
            trainDict['<BOS>'] += 1
            trainDict['<EOS>'] += 1
            for word in lines[i].split():       #每个单词
                word = word.strip()
                totalTrainWordsCnt += 1
                if word in trainDict:
                    trainDict[word] += 1
                else:
                    trainDict[word] = 1

    #将词典输出到文件"dict.txt"
    with codecs.open("dict.txt",'w','UTF-8') as dictFile:
        for key in trainDict:
            dictFile.write(key)
            dictFile.write(' ')
            dictFile.write(str(trainDict[key]))
            dictFile.write('\n')

    return trainDict, totalTrainWordsCnt

def bi_init():
    '求训练预料中各二元词汇出现的频率'
    #得到二元频次，每个词后跟另一个词的频次，每个词形成一个dict，而这些dict合为一个bi_trainDict
    bi_trainDict = dict()
    bi_trainDict['<BOS>'] = 0
    bi_trainDict['<EOS>'] = 0   
    with codecs.open('train.txt','r','UTF-8') as trainFile:
        lines = trainFile.readlines()
        for i in range(0,lines.__len__(),1):    #取出每行单词
            lastWord = '<BOS>'
            for word in lines[i].split():       #每个单词
                word = word.strip()
                bi_word = '{}{}'
                bi_word = bi_word.format(lastWord,word)
                if bi_word not in bi_trainDict:
                    bi_trainDict[bi_word] = 1
                else:
                    bi_trainDict[bi_word] += 1
                lastWord = word
            bi_word = '{}{}'
            bi_word = bi_word.format(lastWord,'<EOS>')
            if bi_word in bi_trainDict:
                bi_trainDict[bi_word] += 1
            else:
                bi_trainDict[bi_word] = 1
            bi_trainDict['<BOS>'] += 1
            bi_trainDict['<EOS>'] += 1 
    
    #存储二元词汇及其频次到文件
    with codecs.open("bi_dict.txt",'w','UTF-8') as bi_dictFile:
        for key in bi_trainDict:
            bi_dictFile.write(key)
            bi_dictFile.write(': ')
            bi_dictFile.write(str(bi_trainDict[key]))
            bi_dictFile.write('\n')

    return bi_trainDict

def tri_init():
    '求训练预料中各三元词汇出现的频率'
    tri_trainDict = dict()  #key值为三元词汇，value为三元词汇频次
    tri_trainDict['<BOS>'] = 0
    tri_trainDict['<EOS>'] = 0  
    with codecs.open('train.txt','r','UTF-8') as trainFile:
        lines = trainFile.readlines()
        for i in range(0,lines.__len__(),1):
            last1word = ''
            last2word = '<BOS>'
            for word in lines[i].split():
                word = word.strip()
                tri_word = '{}{}{}'
                tri_word = tri_word.format(last1word,last2word,word)
                if tri_word not in tri_trainDict:
                    tri_trainDict[tri_word] = 1
                else:
                    tri_trainDict[tri_word] += 1
                last1word = last2word
                last2word = word
            tri_word = '{}{}{}'
            tri_word = tri_word.format(last1word,last2word,'<EOS>')
            if tri_word not in tri_trainDict:
                tri_trainDict[tri_word] = 1
            else:
                tri_trainDict[tri_word] += 1
            tri_trainDict['<BOS>'] += 1
            tri_trainDict['<EOS>'] += 1 
    
    #存储三元词汇及频次到词典
    with codecs.open('tri_dict.txt','w','UTF-8') as tri_dictFile:
        for key in tri_trainDict:
            tri_dictFile.write(key)
            tri_dictFile.write(': ')
            tri_dictFile.write(str(tri_trainDict[key]))
            tri_dictFile.write('\n')

    return tri_trainDict

def trigram():
    '三元trigram'   
    trainDict,totalTrainWordsCnt = uni_init()   #将训练文本"train.txt"中的 词&频次 存储到trainDict中
    bi_trainDict = bi_init()
    tri_trainDict = tri_init()

    with codecs.open("tri_add1PP.txt",'w','UTF-8') as eachLinePP:
        pass
    with codecs.open("tri_backOffPP.txt",'w','UTF-8') as eachLinePP:
        pass
    
    deleteLineCnt = 0
    deleteLine = list()

    #测试 BackOff平滑
    linesCnt = 0            #测试语句行数
    #totalTestWordsCnt = 0   #测试文本总词数
    PPave = 0               #测试文本各行语句平均困惑度
    with codecs.open('test.txt','r','UTF-8') as testFile:
        testLines = testFile.readlines()
        for testLine in testLines:  
            deleteLineCnt += 1      
            pLineLog2 = 0.0         #该行测试语句的概率(log2 P)
            lineSentence = list()   #该行词汇List
            for word in testLine.split():
                word = word.strip()
                lineSentence.append(word)
            lineWordCnt = lineSentence.__len__()
            if lineWordCnt != 0:    #该行不为空
                last1word = ''
                last2word = '<BOS>'
                for i in range(0,lineWordCnt + 1,1):
                    #先求对数，可将求一行语句概率的乘法转换为各单词概率log加法
                    prob = 0.0
                    bi_word = '{}{}'
                    bi_word = bi_word.format(last1word,last2word)
                    tri_word = '{}{}{}'
                    back_biword = '{}{}'
                    current_word = '{}'
                    if i == lineWordCnt:
                        tri_word = tri_word.format(last1word,last2word,'<EOS>')
                        back_biword = back_biword.format(last2word,'<EOS')
                        current_word = current_word.format('<EOS>')
                    else:
                        tri_word = tri_word.format(last1word,last2word,lineSentence[i])
                        back_biword = back_biword.format(last2word,lineSentence[i])
                        current_word = current_word.format(lineSentence[i])
                    #ABC在三元词典里，则二元词典里肯定有AB
                    if (tri_word in tri_trainDict) and (bi_word in bi_trainDict):
                        prob = tri_trainDict[tri_word] / bi_trainDict[bi_word]
                    else:#回退
                        #回退到2gram
                        if (back_biword in bi_trainDict) and (last2word in trainDict):
                            prob = bi_trainDict[back_biword] / trainDict[last2word]
                        else:#退回到1-gram
                            if current_word in trainDict:
                                prob = (trainDict[current_word] + 1) / (totalTrainWordsCnt + len(trainDict))
                            else:
                                prob = 1 / (totalTrainWordsCnt + len(trainDict))
                    
                    if i != lineWordCnt:
                        last1word = last2word
                        last2word = lineSentence[i]
                    pLineLog2 += math.log(prob,2)
                HpT = -(1 / lineWordCnt * pLineLog2)    #该行测试语料的交叉熵
                PPpT = 2 ** HpT                         #改行测试语料的困惑度 
                #totalTestWordsCnt += lineWordCnt
                if PPpT >= 10000:
                    deleteLine.append(deleteLineCnt)
        
        lines = list
        with codecs.open('test.txt','r','UTF-8') as testFile:
            lines = testFile.readlines()
        with codecs.open('test.txt','w','UTF-8') as testFile:
            for i in range(0,len(lines),1):
                if (i + 1) not in deleteLine:
                    testFile.write(lines[i])


    return 

#main program
print('Word Perplexity of \'test.txt\' on average: ')
trigram()
