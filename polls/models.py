from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class AnonymousUser(models.Model):
    id_string = models.TextField()

    def __str__(self):
        return self.id_string


class Poll(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField('date started')
    end_date = models.DateField('date ended')
    # the one who answers
    # user = models.ManyToManyField(AnonymousUser)
    # 

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    field_code = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class PollAnswer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} answered to poll {self.poll}'


class QuestionAnswer(models.Model):
    poll_answer = models.ForeignKey(PollAnswer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f'{self.poll_answer.user} answered to {self.question} with {self.answer_text}'

