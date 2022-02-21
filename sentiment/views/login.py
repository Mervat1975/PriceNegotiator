from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from sentiment.models import SentimentAdmin
from django.views import View


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'sentiment/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin_user = SentimentAdmin.get_admin_by_email(email)
        error_message = None
        if admin_user:
            flag = check_password(password, admin_user.password)
            if flag:
                request.session['admin_user'] = admin_user.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('admin_homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request, 'sentiment/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('admin_login')
