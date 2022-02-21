from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Create your views here.


@login_required
@require_http_methods(['GET'])
def home(request):
    return render(request, 'sentiment/home.html')


@require_http_methods(['GET'])
def review_submission(request):
    return render(request, 'sentiment/review-submission.html')
