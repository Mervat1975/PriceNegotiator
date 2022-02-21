from django.contrib import admin

from sentiment.models import SentimentAdmin, OptionResponse, Question, QuestionOptions, SentimentAdmin, TextResponse

# Register your models here.


class QuestionFormAdmin(admin.ModelAdmin):
    list_display = ('qu_id', 'qu_text', 'qu_type', 'qu_class')


admin.site.register(Question, QuestionFormAdmin)


class QuestionOptionsFormAdmin(admin.ModelAdmin):
    list_display = ('op_id', 'op_text', 'qu_id')


admin.site.register(QuestionOptions, QuestionOptionsFormAdmin)


class TextResponsFormAdmin(admin.ModelAdmin):
    list_display = ('txt_res_id', 'txt_res_text', 'qu_id')


admin.site.register(TextResponse, TextResponsFormAdmin)


class OptionResponsFormAdmin(admin.ModelAdmin):
    list_display = ('op_res_id', 'op_id')


admin.site.register(OptionResponse, OptionResponsFormAdmin)


class SentimentAdminFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name')


admin.site.register(SentimentAdmin, SentimentAdminFormAdmin)
