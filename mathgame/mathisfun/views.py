from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.template import Context, Template
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import fractions
import operator
from .models import Results
# Create your views here.


Users = Results.objects.all()

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('selection')
        else:
            pass
            return HttpResponse('<h1>User not active</h1>')
    else:
        return HttpResponse('<h1>User does not exist</h1>')


@login_required
def selection(request):

    return render(request, 'mathisfun/selection.html')


@login_required
def solver(request):
    ops = {'addition': operator.add,
          'subtraction': operator.sub,
          'multiplication': operator.mul,
          'division': operator.truediv
          }

    #return HttpResponse("Inside solver")
    # left_nom=1&left_denom=2&operator=addition&right_nom=1&right_denom=2
    somevalue = request.GET
    if len(somevalue) == 0:
        return render(request, 'mathisfun/solver.html')
    try:
        for x in somevalue.keys():
            if not somevalue[x]:
                raise AttributeError
        op= somevalue.get('operator',None)
        leftfraction = fractions.Fraction(int(somevalue.get('left_num', None)),int(somevalue.get('left_denom',None)))
        rightfract = fractions.Fraction(int(somevalue.get('right_num', None)), int(somevalue.get('right_denom', None)))
        print(leftfraction)
        print(rightfract)
        resultfract = ops[op](leftfraction,rightfract)
        print(resultfract)
        context = {'result_num':resultfract.numerator,'result_denom':resultfract.denominator,
                   'left_num':leftfraction.numerator, 'left_denom':leftfraction.denominator,
                   'right_num':rightfract.numerator,'right_denom':rightfract.denominator,
                   'operator':op}
        return render(request,'mathisfun/solver.html', context)
    except AttributeError:
        print('Error: Missing an input value')
    except ZeroDivisionError:
        print("Error: Denominator can't be zero!")




@login_required
def quizzer(request):
    #return HttpResponse("Inside quizzer")
    return render(request, 'mathisfun/quizzer.html')


@login_required
def results(request):
    return render(request, 'mathisfun/charts.html', {})


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = {}
        # ***************************************************************
        # This needs to be replaced for the user that is logged in
        currentUser = "<userid>"
        data.setdefault(currentUser,[5,4,6,5,20])
        # ***************************************************************
        data.setdefault("user",currentUser)
        sumScores = [0,0,0,0,0]
        for user in Results.objects.all():
            sumScores[0] = sumScores[0] + user.addition
            sumScores[1] = sumScores[1] + user.subtraction
            sumScores[2] = sumScores[2] + user.multiplication
            sumScores[3] = sumScores[3] + user.division
            sumScores[4] = sumScores[4] + user.total
        count = Users.count()

        averageScores = [
            sumScores[0] / count,
            sumScores[1] / count,
            sumScores[2] / count,
            sumScores[3] / count,
            sumScores[4] / count
        ]
        data.setdefault("all",averageScores)
        return Response(data)


# TODO remove these. they are just for example purposes
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
#
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
