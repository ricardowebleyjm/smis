from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from django.conf import settings

from authentication.forms import LoginForm

def index(request: HttpRequest):
    return render(request, 'base/index.html')

class IndexView(View):
    template_name:str = "base/index.html" 
    
    def get(self, request):
        form = LoginForm()
        context = {
            "form": form,
            "login_error": ""
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST, request=request)

        if form.is_valid():
            user = form.cleaned_data["user"]
            remember = form.cleaned_data["remember_me"]

            login(request, user)

            if remember:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)

            return redirect("dashboard")
        
        return render(request, self.template_name, {"form": form})