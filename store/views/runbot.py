from django.shortcuts import render, redirect


from django.views import View


class RunBot(View):
    def post(self, request):
        return redirect('Main View')
