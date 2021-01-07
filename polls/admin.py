from django.contrib import admin
from polls.models import AnonymousUser, Poll, Question, Choice, PollAnswer, QuestionAnswer
from rest_framework.authtoken.models import Token



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_display = ('question_text', 'poll', 'field_code')
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]
    inlines = [ChoiceInline]


class PollAdmin(admin.ModelAdmin):
    # start_date cannot be edited through admin
    exclude = ('start_date',)
    search_fields = ['name', 'description']
    list_display = ('name', 'description', 'start_date', 'end_date')
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]
    inlines = [QuestionInline]
    


class PollAnswerAdmin(admin.ModelAdmin):
    search_fields = ['poll', 'user']
    list_display = ('poll', 'user')


admin.site.register(AnonymousUser)
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
admin.site.register(PollAnswer, PollAnswerAdmin)
admin.site.register(QuestionAnswer)