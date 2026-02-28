from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.views import View
from .forms import RegisterForm
from .models import User
from encoders.pass_encoder import encoder

from random import choice
from string import ascii_letters, digits
import re


# Create your views here.
def cleared_messages(request: HttpRequest) -> None:
    """ Function cleared a whole messages store. 'request' parameter must be passed. """

    store = messages.get_messages(request)
    store.used = True


class RegisterView(View):
    """
        View responsible for url with registering new users.
        Methods:
            get(request):
                Handles requests of GET type. Sends an HTML with a register form.
            post(request):
                Handles requests of POST type.
                Validates users data, creates user instance in DB and redirects to a login page if data is valid.
                Otherwise, send a register form again.
        Protected methods:
            _pass_validation(password):
                Validates a user password for a forbidden characters.
                parameters:
                    password: String representing a user's password.
            _username_validation(username):
                Validates a username.
                parameters:
                    username: String representing a user's username.
            _unique_identification_creator():
                Generates a unique identifier for the user. No parameters are passed.
    """

    # Pattern for password and username check
    pass_pattern = re.compile('[!@#$%^&()~`<>?/{}\[\]:;"\']')
    username_pattern = re.compile('[A-Za-z0-9_]+')

    def get(self, request):
        form = RegisterForm()
        return render(request, "regst/register.html", context={"form": form})

    def post(self, request):
        user = RegisterForm(request.POST)

        if user.is_valid():
            data = user.cleaned_data

            if not self._username_validation(data['username']):
                cleared_messages(request)
                messages.error(request, 'Username contains forbidden characters!')
                return render(request, 'regst/register.html', {'form': RegisterForm()})

            if not self._pass_validation(data['password']):
                cleared_messages(request)
                messages.error(request, 'Password contains forbidden characters!')
                return render(request, 'regst/register.html', {'form': RegisterForm()})

            if data['password'] != data['repeat_pass']:
                cleared_messages(request)
                messages.error(request, 'Passwords do not match!')
                return render(request, 'regst/register.html', {'form': RegisterForm()})

            encoded_password = encoder(data['password'])

            user_inst = User(
                username=data['username'],
                us_password=encoded_password,
                email=data['email'],
                agent=request.META['HTTP_USER_AGENT'],
                identifier=self._unique_identification_creator())
            try:
                user_inst.save()
            except IntegrityError:
                cleared_messages(request)
                messages.error(request, 'User already exists!')
                return render(request, 'regst/register.html', {'form': RegisterForm()})
            else:
                cleared_messages(request)
                messages.success(request, 'Registration successful! You can log in now.')
                return HttpResponseRedirect('/login')
        else:
            cleared_messages(request)
            messages.error(request, 'Field filling rules violation!')
            return render(request, 'regst/register.html', {'form': RegisterForm()})


    def _username_validation(self, username):
        if self.username_pattern.fullmatch(username):
            return True
        return False


    def _pass_validation(self, password):
        if self.pass_pattern.search(password):
            return False
        return True


    @staticmethod
    def _unique_identification_creator():
        identifier = ''
        for _ in range(15):
            identifier += choice(ascii_letters + digits + '-_+.')
        return identifier

