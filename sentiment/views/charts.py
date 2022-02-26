
from django.shortcuts import render
from django.views import View
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sentiment.models import Question, QuestionOptions, TextResponse, OptionResponse


class Charts(View):
    def get(self, request):
        flag = "0"
        txt_res_count = TextResponse.objects.all().count()
        op_res_count = OptionResponse.objects.all().count()
        all_res_count = op_res_count + txt_res_count

        return render(request, 'sentiment/dashboard.html', {'flag': flag, 'op_res_count': op_res_count, 'txt_res_count': txt_res_count, 'all_res_count': all_res_count})

    def post(self, request):
        flag = "1"
        txt_res_count = TextResponse.objects.all().count()
        op_res_count = OptionResponse.objects.all().count()
        all_res_count = op_res_count + txt_res_count
        post_data = request.POST
        review_class = post_data.get('review-class')
        check_active = post_data.get('check-active')
        type = post_data.get('type')
        from_months = post_data.get('from-months')
        current_date = datetime.today()
        n = int(from_months)
        print(n)
        past_date = current_date - relativedelta(months=n)

        labels = []
        data = []
        qu_name = []
        qu_op_num = []
        qu_id = []
        if(check_active == "active"):
            questions = Question.objects.filter(
                qu_class=review_class).filter(qu_act_status=True)
        else:
            questions = Question.objects.filter(qu_class=review_class)

        for qu in questions:
            qu_id.append(qu.qu_id)
            qu_name.append(qu.qu_text)
            if (qu.qu_type == "O"):
                qu_op_num.append(2)
                labels.append("Positive")
                data.append(TextResponse.objects.filter(qu_id=qu).filter(
                    txt_res_sentiment='positive').filter(txt_res_date__lt=past_date).count())
                labels.append("Negative")
                data.append(TextResponse.objects.filter(qu_id=qu).filter(
                    txt_res_sentiment='negative').filter(txt_res_date__lt=past_date).count())
            else:
                qu_ops = QuestionOptions.objects.filter(qu_id=qu)
                qu_op_num.append(
                    QuestionOptions.objects.filter(qu_id=qu).count())
                for qu_op in qu_ops:
                    labels.append(qu_op.op_text)
                    data.append(
                        OptionResponse.objects.filter(op_id=qu_op).filter(op_res_date__lt=past_date).count())

        return render(request, 'sentiment/dashboard.html',
                      {'from_months': from_months, 'check_active': check_active, 'review_class':  review_class, 'type': type,
                       'qu_id': qu_id, 'questions': questions, 'qu_op_num': qu_op_num, 'qu_name': qu_name,
                       'labels': labels, 'data': data, 'flag': flag, 'op_res_count': op_res_count,
                       'txt_res_count': txt_res_count, 'all_res_count': all_res_count})
