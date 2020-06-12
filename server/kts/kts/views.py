from django.shortcuts import render
from django.http import HttpResponse
from modelsApp.models import QuestionsList
 

def getAllQuestions(request):
    questionsList = QuestionsList.objects.all()    
    #for e in questionsList:
        #print(e.question)
    context={}
    context['questionsList'] = questionsList
    return render(request, 'testHtml.html', context)


def deleteQuestion(request): 
    Qid=request.GET['Qid']
    Q = QuestionsList.objects.get(id=Qid)
    Q.delete()
    context={}
    return render(request, 'testHtml.html', context)


def addQuestion(request):
    request.encoding='utf-8'
    a=['aa',2,'11',60,'1233132','123dwd',7]
    question=request.GET['question']
    questionType=request.GET['questionType']
    knowledgePoint=request.GET['knowledgePoint']
    difficulty=request.GET['difficulty']
    options=request.GET['options'] #此处存疑
    answer=request.GET['answer']
    score=request.GET['score']
    newQuestion = QuestionsList(question=question, questionType=questionType, knowledgePoint=knowledgePoint, difficulty=difficulty, options=options, answer=answer, score=score )
    #测试成功 #newQuestion = QuestionsList(question=a[0], questionType=a[1], knowledgePoint=a[2], difficulty=a[3], options=a[4], answer=a[5], score=a[6] )
    newQuestion.save()
    context={}
    return render(request, 'testHtml.html', context)


def searchQuestion(request):
    request.encoding='utf-8'
    #print(request)
    searchResults = QuestionsList.objects.all()   
    questionTypes=['单选题','多选题','填空题','判断题'] #questionTypes.index(
    if request.GET['questionType']=='全部':
        questionType=-1
    else:
        questionType=request.GET['questionType']   #<input type="radio" name="questionType"> #单选按钮,
    
    knowledgePoints=['毛泽东思想','新民主主义革命理论','社会主义改造理论','社会主义建设道路初步探索理论成果','邓小平理论']#,'三个代表重要思想','科学发展观','习近平新时代思想','中特社总任务','五位一体总体布局']
    if request.GET['knowledgePoint']=='全部':
        knowledgePoint=-1
    else:
        knowledgePoint=request.GET['knowledgePoint']   #<input type="radio" name="knowledgePoint"> #单选按钮
    
    if request.GET['difficulty']=='全部':
        difficulty=-1
    elif request.GET['difficulty']=='易':
        searchResults = searchResults.objects.filter(difficulty__lt=50) #小于   #<input type="radio" name="difficulty"> #单选按钮
    elif request.GET['difficulty']=='难':
        searchResults = searchResults.objects.filter(difficulty__gte=50) #大于等于

    if questionType!=-1:
        searchResults = searchResults.objects.filter(questionType=questionType)
    if knowledgePoint!=-1:
        searchResults = searchResults.objects.filter(knowledgePoint=knowledgePoint)
    context={}
    context['searchResults'] = searchResults
    return render(request, 'testHtml.html', context)


def alterQuestion(request):
    request.encoding='utf-8'
    deleteQuestion(request)
    addQuestion(request)
    """Qid=request.GET['Qid']
    Q = QuestionsList.objects.get(id=Qid)

    Q.question=request.GET['question']
    Q.questionType=request.GET['questionType']
    Q.knowledgePoint=request.GET['knowledgePoint']
    Q.difficulty=request.GET['difficulty']
    Q.options=request.GET['options'] #此处存疑
    Q.answer=request.GET['answer']
    Q.score=request.GET['score']
    Q.save()
    """
    context={}
    return render(request, 'testHtml.html', context)
    
