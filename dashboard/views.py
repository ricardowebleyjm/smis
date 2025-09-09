from django.shortcuts import render
from django.http import HttpRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, View):
    page_title = "Dashboard"
    def get(self, request: HttpRequest):
        context: dict = {
            'page_title': self.page_title,
        }
        return render(request, 'dashboard/index.html', context)