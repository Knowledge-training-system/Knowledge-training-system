from string import punctuation

import math
import random
import re

import os
import sys

from pathlib import Path
import json

def findAll(thestr, substr):
    # 寻找一个字符串中某子串的所有位置
    posList = []
    pos = thestr.find(substr)
    posShift = 0
    while pos != -1:
        posList.append(pos + posShift)
        thestr=thestr[pos+1:]
        posShift += pos + 1
        pos = thestr.find(substr)
    return posList

questionsList=[]
os.chdir(os.path.dirname(__file__))
questiontxtPath = Path('./initquestions.txt')
with open(questiontxtPath, 'r', encoding='UTF-8') as f:
    knowledgePoints=['毛泽东思想','新民主主义革命理论','社会主义改造理论','社会主义建设道路初步探索理论成果','邓小平理论','三个代表重要思想','科学发展观','习近平新时代思想','中特社总任务','五位一体总体布局']
    chapter=-1
    currentType=-1 #-1表示不处于一道题中,0-3表示四种题型
    currentQuestion={}
    questionId=-1
    questionTypes=['单选题','多选题','填空题','判断题']
    options=[]
    isType2answer=0
    type2answerCount=0
    type2Answers=[]
    for line in f:
        #print(1)
        if line == '\n':#为空行
            continue
        if line == '查看解析\n':
            continue
        
        if currentType==-1:
            matchObj1 = re.match(r'第.章测验', line)
            if matchObj1 != None:
                chapter+=1
                continue
            matchObj2 = re.match(r'[0-9]*\.\[(.*)\] (.*)\n', line)
            if matchObj2 == None:
                continue
            else:
                if matchObj2.group(1)=='简答题':
                    currentType=-1
                    continue
                currentType=questionTypes.index(matchObj2.group(1))
                currentQuestion['question']='['+matchObj2.group(1)+'] '+matchObj2.group(2)
                type2answerCount=len( findAll(matchObj2.group(2),'( )') )
                currentQuestion['questionType']=currentType
                currentQuestion['knowledgePoint']=knowledgePoints[chapter]
                isType2answer=0
        elif currentType==0 or currentType==1:
            #单多选题内
            matchObj3 = re.match(r'([A-D]\..*)\n', line)
            if matchObj3 == None:
                matchObj4 = re.match(r'.*正确答案(：|:)(.*)\n', line)
                if matchObj4 == None:
                    continue
                currentQuestion['answer']=matchObj4.group(2)
                questionsList.append(currentQuestion)
                currentQuestion={}
                currentType=-1
                continue
            else:
                options.append(matchObj3.group(1))
                if len(options)==4:
                    currentQuestion['options']=options
                    options=[]
        elif currentType==2:
            #填空题内
            if isType2answer==1:
                matchObj5 = re.match(r'\(\d*\) (.*)', line)
                type2Answers.append(matchObj5.group(1))
                if len(type2Answers) == type2answerCount:
                    currentQuestion['answer']=type2Answers
                    questionsList.append(currentQuestion)
                    type2Answers=[]
                    currentQuestion={}
                    currentType=-1
                continue
            matchObj6 = re.match(r'正确答案(：|:)', line)
            if matchObj6 == None:
                continue
            else:
                isType2answer=1
                continue
        elif currentType==3:
            #判断题内
            #print(line)
            matchObj7 = re.match(r'.*正确答案(：|:)(.*)\n', line)
            if matchObj7 == None:
                continue
            currentQuestion['answer']=matchObj7.group(2)
            questionsList.append(currentQuestion)
            currentQuestion={}
            currentType=-1
            continue


    resultPath = str(Path('./questionsList.json'))
    with open(resultPath, 'w', encoding='UTF-8') as json_file:
        json_file.write(json.dumps(questionsList, ensure_ascii=False, indent=1))

