from django.contrib.auth.models import User, Group
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render 
from django.views import generic
from django.utils import timezone

from rest_framework import viewsets
from rest_framework import permissions
from polls.serializers import AnonymousUserSerializer, PollSerializerWithStartDate, PollSerializer, QuestionSerializer, ChoiceSerializer, UserSerializer, GroupSerializer

from .models import AnonymousUser, Poll, Question, Choice, PollAnswer, QuestionAnswer
import json

from rest_framework.authtoken.models import Token


def generate_token(request):
    token = Token.objects.create(user=User.objects.get(pk=1))
    token.save()
    context = {
        'token': token
    }
    return render(request, 'polls/generate_token.html', context)
    print(token.key)




def get_or_create_current_user(request):
    user_dict = {
        'HTTP_USER_AGENT':  request.META['HTTP_USER_AGENT'],
        'REMOTE_ADDR': request.META['REMOTE_ADDR'],
        'COOKIES': request.COOKIES,
    }
    id_string = json.dumps(user_dict, indent=4)

    try:
        user = AnonymousUser.objects.get(id_string=id_string)
        # user = AnonymousUser.objects.filter(id_string=id_string)
    except (KeyError, AnonymousUser.DoesNotExist):
        user = AnonymousUser(id_string=id_string)
        user.save()
        return user
    else:
        return user


def index(request):
    """
    Return all published polls in a dictionary separating passed and not passed for current user
    """
    template_name = 'polls/index.html'
    user = get_or_create_current_user(request)

    all_polls = Poll.objects.all()

    polls_that_current_user_participated_in = PollAnswer.objects.filter(user=user)

    polls_that_current_user_didnt_participate_in = Poll.objects.all()

    for answered_poll in polls_that_current_user_participated_in:
        polls_that_current_user_didnt_participate_in = polls_that_current_user_didnt_participate_in.exclude(pk=answered_poll.poll.id)

    context = {
        'user': user,
        'not_passed': polls_that_current_user_didnt_participate_in,
        'passed': polls_that_current_user_participated_in
    }
    return render(request, template_name, context)


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Return all published polls.
        """
        return Poll.objects.all()


class ResultsView(generic.DetailView):
    model = PollAnswer
    template_name = 'polls/results.html'


def post_answer(request, pk):
    """
    Here I need to get user's answers and save them to the DB as QuestionAnswer and PollAnswer.
    """
    # get current user
    user = get_or_create_current_user(request)
    # get poll that was answered
    poll = get_object_or_404(Poll, pk=pk)

    try:
        poll_answer = PollAnswer(poll=poll, user=user)
        poll_answer.save()
        questions = poll.question_set.all()

        for question in questions:
            if (question.field_code == 3):
                # multiple choice question
                answers = {}
                for choice in question.choice_set.all():
                    html_input_name = str(question.id) + '_' + str(choice.id)
                    answers[choice.choice_text] = True if (html_input_name in request.POST) else False
                answer_text = json.dumps(answers)
            else:
                html_input_name = str(question.id)
                answer_text = json.dumps(request.POST[html_input_name])
            question_answer = QuestionAnswer(poll_answer=poll_answer, question=question, answer_text=answer_text)
            question_answer.save()
        
    except (KeyError, Poll.DoesNotExist) as exception:
        # Redisplay the poll form.
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
            'exception_text': exception
        })
    else:
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(poll_answer.id,)))


class PollViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be created, viewed, edited, deleted.\n
    POST to create\n
    GET to view\n
    PUT to edit (note, that you cannot edit start_date after the poll is created)\n
    DELETE to delete
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            serializer_class = PollSerializer
        else:
            serializer_class = PollSerializerWithStartDate
        return serializer_class


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be created, viewed, edited, deleted.\n
    POST to create\n
    GET to view\n
    PUT to edit\n
    DELETE to delete\n
    field_code value:\n
    \t1 - text question\n
    \t2 - single choice question\n
    \t3 - multiple choice question\n
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows choices to be created, viewed, edited, deleted.\n
    POST to create\n
    GET to view\n
    PUT to edit\n
    DELETE to delete
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]