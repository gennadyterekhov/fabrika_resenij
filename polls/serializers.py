from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import AnonymousUser, Poll, Question, Choice, PollAnswer, QuestionAnswer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AnonymousUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnonymousUser
        fields = ['url', 'id_string']


class PollSerializerWithStartDate(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ['url', 'name', 'description', 'start_date', 'end_date', 'question_set']


class PollSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ['url', 'name', 'description', 'end_date', 'question_set']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['url', 'question_text', 'poll', 'field_code', 'choice_set']


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ['url', 'choice_text', 'question']