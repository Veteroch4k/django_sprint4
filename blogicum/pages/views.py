from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render

class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'

class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'

def page_not_found(request, exception):
    # 404
    return render(request, 'pages/404.html', status=404)

def csrf_failure(request, reason=''):

    return render(request, 'pages/403csrf.html', status=403)

def server_error(request):
    # 500
    return render(request, 'pages/500.html', status=500)