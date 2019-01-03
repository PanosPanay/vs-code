import re
import codecs
#词性标注，采用5倍交叉验证

def train(testOrder):
    '用语料库训练得到HMM的参数：转移概率，输出概率，初始状态分布...参数testOrder为用作测试的文本序号'
    InitialStateDict = dict()   #存储初始状态分布的词典，key=词性，value=频次
    TransitionDict = dict()     #存储词性转移频次的词典，key=词性，value也是一个dict：key=下一个词性，value=频次
    ObservationDict = dict()    #存储词性->观察词汇的输出频次的词典，key=词性，value也是一个dict：key=单词，value=频次
    TransitionDict['<BOS>'] = dict()
    InitialStateDict['<BOS>'] = 0
    InitialStateDict['<EOS>'] = 0
    for i in range(1,6,1):#循环1-5各训练文本，用testOrder以外的4各文本训练
        if i != testOrder:
            trainFileName = 'train{}.txt'
            trainFileName = trainFileName.format(str(i))
            with codecs.open(trainFileName,'r','UTF-8') as trainFile:
                trainLines = trainFile.readlines()
                for line in trainLines:
                    InitialStateDict['<BOS>'] += 1
                    InitialStateDict['<EOS>'] += 1
                    lastTag = '<BOS>'
                    for part in line.split():    
                        part = part.strip()
                        parted = re.split('/',part)
                        word = parted[0]
                        tag = parted[1]
                        if tag in InitialStateDict:
                            InitialStateDict[tag] += 1
                        else:
                            InitialStateDict[tag] = 1

                        if tag not in TransitionDict:
                            TransitionDict[tag] = dict()
                        if tag in TransitionDict[lastTag]:
                            TransitionDict[lastTag][tag] += 1
                        else:
                            TransitionDict[lastTag][tag] = 1
                        
                        if tag not in ObservationDict:
                            ObservationDict[tag] = dict()
                        if word in ObservationDict[tag]:
                            ObservationDict[tag][word] += 1
                        else:
                            ObservationDict[tag][word] = 1

                        lastTag = tag  

                    if '<EOS>' not in TransitionDict[lastTag]:
                        TransitionDict[lastTag]['<EOS>'] = 1
                    else:
                        TransitionDict[lastTag]['<EOS>'] += 1
    
    return InitialStateDict,TransitionDict,ObservationDict

def writeDictToFiles(InitialStateDict,TransitionDict,ObservationDict):
    '打印训练出的3个词典'
    with codecs.open('initialState.txt','w','UTF-8') as initialStateFile:
        for key in InitialStateDict:
            initialStateFile.write(key)
            initialStateFile.write(': ')
            initialStateFile.write(str(InitialStateDict[key]))
            initialStateFile.write('\n')

    with codecs.open('transition.txt','w','UTF-8') as transitionFile:
        for key in TransitionDict:
            transitionFile.write(key)
            transitionFile.write(': ')
            for wordKey in TransitionDict[key]:
                transitionFile.write(wordKey)
                transitionFile.write('/')
                transitionFile.write(str(TransitionDict[key][wordKey]))
                transitionFile.write('  ')
            transitionFile.write('\n')

    with codecs.open('observation.txt','w','UTF-8') as observationFile:
        for key in ObservationDict:
            observationFile.write(key)
            observationFile.write(': ')
            for wordKey in ObservationDict[key]:
                observationFile.write(wordKey)
                observationFile.write('/')
                observationFile.write(str(ObservationDict[key][wordKey]))
                observationFile.write('  ')
            observationFile.write('\n\n')

    return

def test(testOrder,InitialStateDict,TransitionDict,ObservationDict):
    '采用viterbi算法，对测试文本进行词性标注'
    testFileName = 'train{}.txt'
    testFileName = testFileName.format(str(testOrder))
    with codecs.open(testFileName,'w','UTF-8') as testFile:
        testLines = testFile.readlines()
        for testline in testLines:            
            lineList = list()       #记录一行的单词
            Viterbi = dict()        #Viterbi词典的key=tag词性（状态j），value是一个dict：key=1 to T（T为观察序列的长度）即时刻t，value=t时刻到达状态j的viterbi路径的概率
            Backpointers = dict()   #记录概率最大路径上当前状态的前一个状态,key=tag词性（状态j），value是一个dict：key=1 to T（T为观察序列的长度）即时刻t，value=概率最大路径上当前状态的前一个状态

            for part in testline.split:
                #分词跳过词性标注，只取单词
                part = part.strip()
                parted = re.split('/',part)
                word = parted[0]
                lineList.append(word)
            #初始化
            for tagStateKey in InitialStateDict:
                if (tagStateKey != '<BOS>') and (tagStateKey != '<EOS>'):
                    Viterbi[tagStateKey] = dict()
                    Viterbi[tagStateKey][1] = (TransitionDict['<BOS>'].get(tagStateKey,0) / InitialStateDict['<BOS>']) * (ObservationDict[tagStateKey].get(lineList[0],0) / InitialStateDict[tagStateKey])
                    Backpointers[tagStateKey] = dict()
                    Backpointers[tagStateKey][1] = 0
            #归纳运算
            for time in range(2,len(lineList) + 1,1):
                for stateKey in InitialStateDict:
                    if (stateKey != '<BOS>') and (stateKey != '<EOS>'): 
                        perhapsProbDict = dict()         #用来记录归纳运算中每个可能的概率及其对应的上一状态（词性）             
                        for lastState in InitialStateDict:
                            if (lastState != '<BOS>') and (lastState != '<EOS>'):
                                v = Viterbi[lastState][time - 1] * (TransitionDict[lastState].get(stateKey,0) / InitialStateDict[lastState]) * (ObservationDict[stateKey].get(lineList[time - 1],0) / InitialStateDict[stateKey])
                                perhapsProbDict[lastState] = v
                        Backpointers[stateKey][time] = max(perhapsProbDict,key = perhapsProbDict.get)
                        Viterbi[stateKey][time] = perhapsProbDict[Backpointers[stateKey][time]]
            #结束
            perhapsProbDict = dict()         #用来记录每个可能的概率及其对应的状态（词性）
            for state in InitialStateDict:
                if (state != '<BOS>') and (state != '<EOS>'):
                    v = Viterbi[state][len(lineList)] * (TransitionDict[state].get('<EOS>',0) / InitialStateDict[state])
                    perhapsProbDict[state] = v
            Backpointers['<EOS>'][len(lineList)] = max(perhapsProbDict,key = perhapsProbDict.get)
            Viterbi['<EOS>'][len(lineList)] = perhapsProbDict[Backpointers['<EOS>'][len(lineList)]]

    #求正确率，并返回correctRate = 
    return

#main program
for i in range(1,6,1):
    InitialStateDict,TransitionDict,ObservationDict = train(i)
    writeDictToFiles(InitialStateDict,TransitionDict,ObservationDict)
    test(i,InitialStateDict,TransitionDict,ObservationDict)