from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from sentiment.models import Question, QuestionOptions, TextResponse, OptionResponse
from django.views import View
from sentiment.ai.predection import predict_sentiment


class Review(View):
    return_url = None

    def get(self, request):
        get_data = request.GET

        if (get_data.get("flag") == "0"):
            questions = Question.get_web_act_Question()

        else:
            questions = Question.get_all_act_Question()

        print("question:", questions)

        options = QuestionOptions.get_all_QuestionOptions()
        request.session['flag'] = get_data.get("flag")

        return render(request, 'sentiment/review.html', {'questions': questions, 'options': options, 'flag': get_data.get("flag")})

    def post(self, request):

        post_data = request.POST
        print("Post", post_data)
        print("flag", request.session['flag'])

        if (request.session['flag'] == "0"):
            questions = Question.get_web_act_Question()

        else:
            questions = Question.get_all_act_Question()

        for qu in questions:
            qu_ans = post_data.get(str(qu.qu_id))

            if qu.qu_type is "O":
                predict = predict_sentiment(qu_ans)
                ans = TextResponse(txt_res_text=qu_ans,
                                   txt_res_sentiment=predict,
                                   qu_id=qu)
                ans.saveTextRes()
            else:
                print("options", QuestionOptions.objects.filter(op_id=int(qu_ans)))
                ans = OptionResponse(
                    op_id=QuestionOptions.objects.filter(op_id=int(qu_ans))[0])
                ans.saveOpRes()

        return render(request, 'sentiment/review-submission.html')
