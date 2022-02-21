from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from sentiment.models import Question, QuestionOptions, TextResponse, OptionResponse
from django.views import View


class Review(View):
    return_url = None

    def get(self, request):
        questions = Question.get_all_act_Question()
        options = QuestionOptions.get_all_QuestionOptions()

        return render(request, 'sentiment/review.html', {'questions': questions, 'options': options})

    def post(self, request):
        post_data = request.POST
        print("Post", post_data)
        questions = Question.get_all_act_Question()
        for qu in questions:
            qu_ans = post_data.get(str(qu.qu_id))
            print(qu_ans)

            if qu.qu_type is "O":
                ans = TextResponse(txt_res_text=qu_ans,
                                   txt_res_sentiment="is not determined yet",
                                   qu_id=qu)
                ans.saveTextRes()
            else:
                print("options", QuestionOptions.objects.filter(op_id=int(qu_ans)))
                ans = OptionResponse(
                    op_id=QuestionOptions.objects.filter(op_id=int(qu_ans))[0])
                ans.saveOpRes()

        return render(request, 'sentiment/review-submission.html')
