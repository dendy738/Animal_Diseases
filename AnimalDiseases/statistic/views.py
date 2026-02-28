from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from regst.views import cleared_messages
from pathlib import Path
from AnimalDiseases.settings import BASE_DIR


# Create your views here.

class StatisticView(View):
    """
        View responsible for url where user chooses animal type whose statistics would like to look at.
        Methods:
            get(request):
                Handles requests of GET type. If user not logged in - redirect to login page.
                Sends a form with choice of animal.
    """

    def get(self, request, idn):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')

        if Path(str(BASE_DIR) + f'/user_statistic/static/images/user_{idn}_statistic.png').exists():
            Path(str(BASE_DIR) + f'/user_statistic/static/images/user_{idn}_statistic.png').unlink()

        types = ['Dog', 'Cat', 'Cow', 'Pig', 'Rabbit', 'Sheep', 'Goat', 'Horse']
        return render(request, 'statistic/animal_choice.html', {'animals': types, 'idn': idn})


class CertainAnimalView(View):
    """
        View responsible for url where user chooses type of statistic based on animal features or general statistic.
        Methods:
            get(request):
                Handles requests of GET type. If user not logged in - redirect to login page.
                Sends a form with choice of type of statistic.
    """

    def get(self, request, idn, pet):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')
        return render(request, 'statistic/feature_choice.html', {'idn': idn, 'pet': pet})


class StatisticPlotView(View):
    """
        View responsible for url where plot of statistic is shown.
        Methods:
            get(request):
                Handles requests of GET type. If user not logged in - redirect to login page.
                Sends a template with plot of statistic.
    """

    def get(self, request, idn, pet, feat):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')
        return render(request, f'statistic/{pet}/{pet}_{feat}_stat.html', {'idn': idn, 'pet': pet, 'feat': feat})


