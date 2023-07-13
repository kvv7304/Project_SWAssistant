from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from backoffice import table_main, backoffice  # noqa
from django_app.forms import RegistrationForm, LoginForm


class MyLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page:
            return next_page
        return reverse('table_main')  # Замените 'table_main' на имя вашего URL-шаблона главной страницы

class CustomLoginView(LoginView):
    template_name = 'registration.html'
    authentication_form = LoginForm

class CustomRegisterView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    model = get_user_model()

class CustomRegisterView(FormView):
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
        number = request.user.sw_numer
        password = request.user.sw_password
        pk = request.user.pk
        name = request.user.first_name
        error = backoffice(number, password, pk, name, request)
        if error:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            context = {
                'table_data': None,
                'name': error,  # передаем ошибку в name
                'last_modified': current_time,
            }
            return render(request, 'main.html', context)

        else:
            return redirect('table_main')

def save(request):
    if request.method == 'POST':
        if 'fill_fields' in request.POST:
            # Получение текущего пользователя (можно изменить на вашу логику получения пользователя)
            user = request.user
            # Заполнение полей пользователя
            user.first_name = request.POST.get('first_name')
            user.sw_numer = request.POST.get('sw_numer')
            user.sw_password = request.POST.get('sw_password')
            user.save()
            # Перенаправление пользователя на другую страницу или ту же страницу
            # return redirect('table_main')  # Измените URL на нужный вам
            return load(request)

    return render(request, 'table_main.html', {'user': request.user})

def my_logout(request):
    logout(request)
    return redirect('table_main')  # Замените 'table_main' на имя вашего URL-шаблона главной страницы
