from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from sentiment.models import SentimentAdmin
from django.views import View


class Signup(View):
    def get(self, request):
        print("hi")
        return render(request, 'sentiment/signup.html')

    def post(self, request):
        post_data = request.POST
        first_name = post_data.get('firstname')
        last_name = post_data.get('lastname')
        email = post_data.get('email')
        password = post_data.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        error_message = None

        admin_user = SentimentAdmin(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password)
        error_message = self.validate_admin_user(admin_user)

        if not error_message:
            print(first_name, last_name, email, password)
            admin_user.password = make_password(admin_user.password)
            admin_user.register()
            return redirect('admin_homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'sentiment/signup.html', data)

    def validate_admin_user(self, admin_user):
        error_message = None
        if not admin_user.first_name:
            error_message = "Please Enter your First Name mmmm!!"
        elif len(admin_user.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not admin_user.last_name:
            error_message = 'Please Enter your Last Name'
        elif len(admin_user.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif len(admin_user.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(admin_user.email) < 5:
            error_message = 'Email must be 5 char long'
        elif admin_user.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
