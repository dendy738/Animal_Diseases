from pathlib import Path

from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.views import View
from django.contrib import messages

from .forms import LoginForm
from regst.models import User
from regst.views import cleared_messages
from encoders.pass_encoder import encoder, decoder
from AnimalDiseases.settings import BASE_DIR

import re


# Create your views here.

class LoginView(View):
    """
        View responsible for url with authorization new users.
        Methods:
            get(request):
                Handles requests of GET type. Clears all sessions and sends login form.
            post(request):
                Handles requests of POST type.
                Firstly validates users data and if data is valid redirects to a main page.
    """

    def get(self, request):
        us_idn = request.session.get('user')
        if us_idn:
            if Path(str(BASE_DIR) + f'/user_statistic/static/images/user_{us_idn}_statistic.png').exists():
                Path(str(BASE_DIR) + f'/user_statistic/static/images/user_{us_idn}_statistic.png').unlink()

        request.session.flush()
        cleared_messages(request)
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})


    def post(self, request):
        user_data = LoginForm(request.POST)
        if user_data.is_valid():
            clean = user_data.cleaned_data
            try:
                user = User.objects.get(username=clean['username'])
            except User.DoesNotExist:
                cleared_messages(request)
                messages.error(request, 'User not found!')
                return render(request, 'login/login.html', {'form': LoginForm()})
            else:
                if decoder(user.us_password) == clean['password']:
                    request.session['user'] = user.identifier
                    return HttpResponseRedirect(f'/{user.identifier}/main/')
                else:
                    cleared_messages(request)
                    messages.error(request, 'Incorrect password!')
                    return render(request, 'login/login.html', {'form': LoginForm()})
        else:
            cleared_messages(request)
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login/login.html', {'form': LoginForm()})


class EmailView(View):
    """
        View responsible for url with a username field and email field for check if user exists.
        Methods:
            get(request):
                Handles requests of GET type. Sends a form with username and email fields.
            post(request):
                Handles requests of POST type. Verify if user exists for the opportunity to change data of the user.
    """

    def get(self, request):
        return render(request, 'login/email.html')

    def post(self, request):
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)

        if not email or not username:
            cleared_messages(request)
            messages.error(request, 'Fields must be filled!')
            return render(request, 'login/email.html')
        else:
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                cleared_messages(request)
                messages.error(request, 'User not found!')
                return render(request, 'login/email.html')
            else:
                return HttpResponseRedirect(f'/login/reset_password/{user.id}')


class ResetPasswordView(View):
    """
        View responsible for getting a new data for change a password.
        Methods:
            get(request):
                Handles requests of GET type. Sends a form for changing password.
            post(request):
                Handles requests of POST type. New password validation procedure and changing data of particular user.
        Protected methods:
            _is_valid_password(password):
                Checks if the new password is valid.
                parameters:
                password: String representing a user's new password.
    """

    pass_pattern = re.compile(r'[!@#$%^&()~`<>?/\\{}\[\]:;\"\']')

    def get(self, request, pk):
        return render(request, 'login/reset_password.html')

    def post(self, request, pk):
        new_pass = request.POST.get('password', None)
        repeat = request.POST.get('repeat', None)

        if not new_pass or not repeat:
            cleared_messages(request)
            messages.error(request, 'Fields must be filled!')
            return render(request, 'login/reset_password.html')

        if not self._is_valid_password(new_pass):
            cleared_messages(request)
            messages.error(request, 'Invalid password!')
            return render(request, 'login/reset_password.html')

        if new_pass != repeat:
            cleared_messages(request)
            messages.error(request, 'Passwords do not match!')
            return render(request, 'login/reset_password.html')

        try:
            user = User.objects.filter(id=pk).update(us_password=encoder(new_pass))
        except:
            cleared_messages(request)
            messages.error(request, 'Something went wrong! Try again later.')
            return render(request, 'login/reset_password.html')
        else:
            cleared_messages(request)
            messages.success(request, 'Your password was successfully updated! You can log in now.')
            return HttpResponseRedirect('/login')


    def _is_valid_password(self, password):
        if self.pass_pattern.search(password):
            return False
        return True





