import re
import codecs
def evaluation(resultFileName,answerFileName):#输出分词结果文件，正确分词答案文件
    "评价程序，直接将一行分词结果和答案取交集，算该行正确分词数"
    correct_segmented = 0
    words_segmention = 0
    words_reference = 0
    with codecs.open(resultFileName,'r','UTF-8') as resultFile:
        with codecs.open(answerFileName,'r','UTF-8') as answerFile:
            resultLines=resultFile.readlines()
            answerLines=answerFile.readlines()
            for i in range(0,answerLines.__len__(),1):
                resultLineSet = set()
                answerLineSet = set()
                for word in resultLines[i].split():
                    word = word.strip()
                    resultLineSet.add(word)
                for word in answerLines[i].split():
                    word = word.strip()
                    answerLineSet.add(word)
                correctLineSet = resultLineSet & answerLineSet
                correct_segmented += correctLineSet.__len__()
                words_segmention += resultLineSet.__len__()
                words_reference += answerLineSet.__len__()
    precision = float(correct_segmented / words_segmention)
    recall = float(correct_segmented / words_reference)
    Fmeasure = 2 * precision * recall / (precision + recall)
    return precision, recall, Fmeasure

#将训练文本"train.txt"中的词存储到trainSet中
trainSet = set()
with codecs.open('train.txt','r','UTF-8') as trainFile:
    lines=trainFile.readlines()
    #取出每行单词
    for i in range(0,lines.__len__(),1):
        for word in lines[i].split():
            word = word.strip()
            trainSet.add(word)

#将trainSet中的词存储到文件，执行一次即可
""" with codecs.open('trainSet.txt','w','UTF-8') as dictFile:
    for word in trainSet:
        dictFile.write(word)
        dictFile.write('\n') """

#正向最大匹配
wordSeg = []
max_length = 20             #最大匹配长度
with codecs.open('test.txt','r','UTF-8') as testFile:
    with codecs.open('testforward_out.txt','w','UTF_8') as testOutFile:
        lines = testFile.readlines()
        for line in lines:
            line = line.strip()#删除空白符（包括'\n', '\r',  '\t',  ' ')
            start = 0
            while start < len(line):
                current_length = max_length
                while current_length > 0 :
                    end = start + current_length - 1
                    if end >= line.__len__():
                        current_length = current_length -1
                    else:
                        testSeg = line[start : end + 1]
                        if testSeg in trainSet:#词表中存在该词
                            testOutFile.write(testSeg)
                            testOutFile.write(' ')
                            start = end + 1
                            current_length = -1 #使退出循环
                        else: #词表中不存在该词
                            current_length = current_length -1
                if current_length == 0: #词典中不存在这个字
                    testOutFile.write(line[start])
                    testOutFile.write(' ')
                    start = start + 1
            testOutFile.write('\n')

print ('正向最大匹配中文分词Evaluation Metrics:')
precision, recall, Fmeasure = evaluation('testforward_out.txt','test_true_result.txt')
print ('Precision = ' , precision)
print ('Recall = ' , recall)
print ('F measure = ' , Fmeasure) 

#逆向最大匹配
wordSeg = []
max_length = 20             #最大匹配长度
with codecs.open('test.txt','r','UTF-8') as testFile:
    with codecs.open('testinverse_out.txt','w','UTF_8') as testOutFile:
        lines = testFile.readlines()
        for line in lines:
            line = line.strip()#删除空白符（包括'\n', '\r',  '\t',  ' ')
            start = len(line) - 1
            temp = []
            while start >= 0:
                current_length = max_length
                while current_length > 0 :
                    end = start - current_length
                    if end < 0:
                        current_length = current_length - 1
                    else:
                        testSeg = line[end : start + 1]
                        if testSeg in trainSet:#词表中存在该词
                            temp.append(testSeg)
                            start = end - 1
                            current_length = -1 #使退出循环
                        else: #词表中不存在该词
                            current_length = current_length -1
                if current_length == 0: #词典中不存在这个字
                    temp.append(line[start])
                    start = start - 1
            i = temp.__len__() - 1
            while i >= 0:
                testOutFile.write(temp[i])
                testOutFile.write(' ')
                i -= 1
            testOutFile.write('\n')

print ('逆向最大匹配中文分词Evaluation Metrics:')
precision, recall, Fmeasure = evaluation('testinverse_out.txt','test_true_result.txt')
print ('Precision = ' , precision)
print ('Recall = ' , recall)
print ('F measure = ' , Fmeasure) 