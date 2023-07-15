from django.contrib.auth import get_user_model, authenticate, login, logout
import threading

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from backoffice import table_main, backoffice  # noqa
from django_app.forms import RegistrationForm, LoginForm

from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'registration.html'
    authentication_form = LoginForm


class CustomRegisterView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    model = get_user_model()


class CustomFormView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('table_main')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

def load(request):
    if request.method == 'POST':
        user = request.user
        error = backoffice(user.sw_numer, user.sw_password, user.pk, user.first_name, request)
        if error:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            context = {
                'table_data': None,
                'name': error,
                'last_modified': current_time,
            }
            return render(request, 'main.html', context)
        else:
            return redirect('table_main')

def save(request):
    if request.method == 'POST':
        if 'fill_fields' in request.POST:
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.sw_numer = request.POST.get('sw_numer')
            user.sw_password = request.POST.get('sw_password')
            user.save()
            return load(request)
    return render(request, 'table_main.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('table_main')
