from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from .forms import AnimalTypeForm, SymptomsForm
from .models import UsersActions
from AnimalDiseases.settings import BASE_DIR
from regst.views import cleared_messages
from regst.models import User

import pandas as pd
import numpy as np
import pickle
from .phrases import PHRASES
from random import choice
import another_transformers
from pathlib import Path
from collections import Counter
import asyncio

# Create your views here.

class AnimalTypeView(View):
    """
        View responsible for url where user chooses animal type.
        Methods:
            get(request, idn):
                Handles requests of GET type. If user not logged in - redirect to login page. Sends a form with choice of animal.
            post(request, idn):
                Handles requests of POST type. Validates data and if data is clean - redirect to next page.
    """

    def get(self, request, idn):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')

        if Path(str(BASE_DIR) + f'/user_statistic/static/images/user_{idn}_statistic.png').exists():
            Path(str(BASE_DIR) + f'/user_statistic/static/images/user_{idn}_statistic.png').unlink()

        animal = AnimalTypeForm()
        return render(request, 'main_app/animal_type.html', {'form': animal, 'idn': idn})


    def post(self, request, idn):
        animal = AnimalTypeForm(request.POST)
        if animal.is_valid():
            data = animal.cleaned_data
            animal_type = data.get('animal_type')
            return HttpResponseRedirect(f'/{idn}/main/{animal_type}')
        else:
            return HttpResponse('Invalid data.')



class DiseaseSymptomsView(View):
    """
        View responsible for url where user inputs symptoms of disease.
        Methods:
            get(request, idn, pet):
                Handles requests of GET type. If user not logged in - redirect to login page. Sends a form with symptoms choices.
            post(request, idn, pet):
                Handles requests of POST type. Validates data and if data is clean - creates a DataFrame and does a disease prediction.
                Each query of each user will be entered into DB.
        Protected methods:
            async _fetch_data(file_name):
                Asynchronous function for read file.
                parameters:
                    file_name: File name that will be read.
            async _fetch_animals_data():
                Asynchronous function for read file that reads all necessary data files.
            async _fetch_model(file_name, n_model):
                Asynchronous function for fetch model from file.
                Fetch the data from 'file_name' and sets the instance attribute if the format 'self.model_{n_model}'.

                parameters:
                    file_name: File name that stores model data.
                    n_model: Model number that will be set as instance attribute in the format 'self.model_{n_model}'
            async _models_integration():
                Asynchronous function that fetches all necessary models.
            _main_fetch_data():
                Main function that activate event loops for all coroutines.
                Hierarchical structure:
                              _main_fetch_data()
                             /                 \
              _fetch_animals_data()         _models_integration()
                       /                           \
                _fetch_data()                  _fetch_model()

            async _prediction(model, inst):
                Asynchronous function for prediction.
                parameters:
                    model: Model object which will do prediction.
                    inst: Instance whose characteristics will be used for prediction.
            async _main_prediction(inst):
                Coroutine function that will asynchronously run async _prediction(model, inst) function.
                Parameter 'inst' is exactly parameter which will be passed into async _prediction(model, inst) function.
            __most_popularity(predictions):
                Function that count the number of each prediction and return the most popular.
                parameters:
                    predictions: List or array like object which contain a predictions.
    """

    animals = None
    animals_by_number = None
    diseases = None

    def get(self, request, idn, pet):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')

        symptoms = SymptomsForm(pet)
        return render(request, 'main_app/animal_info.html', {'form': symptoms, 'idn': idn})


    def post(self, request, idn, pet):
        animal_inst = [pet]
        symp_form = SymptomsForm(pet, request.POST)
        if symp_form.is_valid():
            data = symp_form.cleaned_data

            for k, v in data.items():
                if k == 'breed':
                    if len(v) == 1:
                        breed = float(str(pet) + f'.0{v}')
                    else:
                        breed = float(str(pet) + f'.{v}')
                    animal_inst.append(breed)
                    continue
                else:
                    if v:
                        animal_inst.append(int(v))
                    else:
                        animal_inst.append(np.nan)
                    continue

            self._main_fetch_data()
            user = User.objects.get(identifier=idn)

            if sum(animal_inst[2:-1]) == 0 and animal_inst[-1] < 130:
                user.usersactions_set.create(animal=self.animals_by_number[pet])
                cleared_messages(request)
                messages.success(request, 'Your pet completely healthy!')
                return HttpResponseRedirect(f'/{idn}/main/{pet}/result')

            animal_df = pd.DataFrame(np.array(animal_inst).reshape(1, -1), columns=self.animals.columns[:-1])

            preds = asyncio.run(self._main_prediction(animal_df))

            common_pred = self._most_popularity(preds)

            disease = [d for d, n in self.diseases.items() if n == common_pred][0]

            user.usersactions_set.create(animal=self.animals_by_number[pet], result=disease)

            cleared_messages(request)
            messages.info(request, choice(PHRASES) + disease)
            return HttpResponseRedirect(f'/{idn}/main/{pet}/result')
        else:
            cleared_messages(request)
            messages.error(request, 'Entered data not valid.')
            return render(request, 'main_app/animal_info.html', {'form': SymptomsForm(pet), 'idn': idn})


    async def _fetch_data(self, file_name):
        with open(str(BASE_DIR.parent) + f'/Animal_data/{file_name}', 'rb') as file:
            data = pickle.load(file)
            if 'number' in file_name:
                data = dict((n, a) for a, n in data.items())
        setattr(self, file_name.split('.')[0], data)


    async def _fetch_animals_data(self):
        for file_name in ('animals.pkl', 'diseases.pkl', 'animals_by_number.pkl'):
            await asyncio.create_task(self._fetch_data(file_name))


    async def _fetch_model(self, file_name, n_model):
        with open(str(BASE_DIR.parent) + f'/Models/{file_name}', 'rb') as file:
            setattr(self, f'model_{n_model}', pickle.load(file))


    async def _models_integration(self):
        for n, model in enumerate(('Final_Forest.pkl', 'Final_KNN.pkl', 'Final_Tree.pkl'), start=1):
            await asyncio.create_task(self._fetch_model(model, n))


    def _main_fetch_data(self):
        asyncio.run(self._fetch_animals_data())
        asyncio.run(self._models_integration())


    @staticmethod
    async def _prediction(model, inst):
        pred = model.predict(inst)
        return pred


    async def _main_prediction(self, inst):
        results = []
        for model in (self.model_1, self.model_2, self.model_3):
            task = asyncio.create_task(self._prediction(model, inst))
            results.append(await task)
        return results


    @staticmethod
    def _most_popularity(predictions):
        unpacked = []
        for x in predictions:
            unpacked += list(x)

        result = Counter(unpacked)
        return tuple(result.keys())[0]


class ResultView(View):
    """
        View responsible for url with prediction result.
        Methods:
            get(request, idn, pet):
                Handles requests of GET type. If user not logged in - redirect to login page.
                Sends template which contains a prediction result.
    """

    def get(self, request, idn, pet):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')
        return render(request, 'main_app/result.html', {'idn': idn})
