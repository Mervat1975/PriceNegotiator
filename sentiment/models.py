from optparse import Option
from django.db import models
import datetime
# Create your models here.


class Question(models.Model):
    CLOSED = 'C'
    OPEN = 'O'
    TYPE_CHOICES = [
        (CLOSED, 'Closed end question'),
        (OPEN, 'Open end question')
    ]
    BOT = 'B'
    WEBSITE = 'W'
    CLASS_CHOICES = [
        (BOT, 'Chatbot review'),
        (WEBSITE, 'Website review')
    ]
    qu_id = models.AutoField(primary_key=True)
    qu_text = models.CharField(max_length=100)
    qu_type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    qu_class = models.CharField(max_length=25, choices=CLASS_CHOICES)
    qu_act_status = models.BooleanField(default=True, null=False,
                                        blank=False)

    @staticmethod
    def get_all_Question():
        return Question.objects.all().order_by('qu_id')

    def get_all_act_Question():
        return Question.objects.filter(qu_act_status=True).order_by('qu_id')

    def __str__(self):
        return self.qu_text


class QuestionOptions(models.Model):
    op_id = models.AutoField(primary_key=True)
    op_text = models.CharField(max_length=50)
    qu_id = models.ForeignKey(
        Question, related_name='Question', on_delete=models.CASCADE)

    @staticmethod
    def get_all_optionsByQuestion(qu_id):
        return QuestionOptions.objects.filter(qu_id=qu_id).order_by('op_id')

    def get_one_QuestionOption(op_id):
        return OptionResponse.objects.filter(op_id=op_id)

    def get_all_QuestionOptions():
        return QuestionOptions.objects.all().order_by('op_id')

    def __str__(self):
        return self.op_text


class TextResponse(models.Model):
    txt_res_id = models.AutoField(primary_key=True)
    txt_res_date = models.DateField(default=datetime.datetime.today)
    txt_res_text = models.CharField(max_length=200)
    txt_res_sentiment = models.CharField(max_length=50)
    qu_id = models.OneToOneField(Question, related_name='QuestionText', on_delete=models.CASCADE, null=False,
                                 blank=False)

    # to save the data
    def saveTextRes(self):
        self.save()

    @staticmethod
    def get_all_TextResponse():
        return TextResponse.objects.all().order_by('txt_res_id')

    def __str__(self):
        return self.txt_res_text


class OptionResponse(models.Model):
    op_res_id = models.AutoField(primary_key=True)
    op_res_date = models.DateField(default=datetime.datetime.today)
    op_id = models.ForeignKey(QuestionOptions, related_name='Option', on_delete=models.CASCADE, null=False,
                              blank=False)
    # to save the data

    def saveOpRes(self):
        self.save()

    @staticmethod
    def get_all_OptionResponse():
        return OptionResponse.objects.all().order_by('op_res_id')

    def __str__(self):
        return self.op_id.op_text


class SentimentAdmin(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    # to save the data
    def register(self):
        self.save()

    @staticmethod
    def get_admin_by_email(email):
        try:
            return SentimentAdmin.objects.get(email=email)
        except:
            return False

    @staticmethod
    def get_admin_by_id(id):
        try:
            return SentimentAdmin.objects.get(id=id)
        except:
            return False

    def isExists(self):
        if SentimentAdmin.objects.filter(email=self.email):
            return True

        return False
