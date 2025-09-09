from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from authentication.forms import LoginForm

class LoginView(View):
    template_name:str = "base/index.html" 
    
    def get(self, request):
        form = LoginForm()
        context = {
            "form": form,
            "login_error": ""
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form: LoginForm = LoginForm(request.POST, request=request)
        context = {
            "form": form
        }

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")

            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if not user.is_active:
                    context["login_error"] = "You are not allowed to login. Please contact the administrator."
                    return render(request, self.template_name, context)

                login(request, user)

                if remember:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    request.session.set_expiry(0)

                return redirect("dashboard")
            else:
                context["login_error"] = "Invalid email or password"
                return render(request, self.template_name, context)
        else:
            context["login_error"] = "Invalid email or password"
            return render(request, self.template_name, context)