from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from main_app.models import UsersActions
from regst.views import cleared_messages

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import asyncio

# Create your views here.
mpl.use('Agg')


class UserStatisticView(View):
    """
        View responsible for url with personal statistic for each user.
        Methods:
            get(request, idn):
                Handles requests of GET type. If user not logged in - redirect to login page.
                Fetch all data from DB for particular user and creates personal statistic.
        Protected methods:
            async _plot_create(df, user):
                Asynchronous function for plot create.
                parameters:
                    df: DataFrame. Plot will be created based on this DataFrame.
                    user: unique identifier of user required for saving plot.
            async _create_statistic(df):
                Asynchronous function for create statistic.
                parameters:
                    df: DataFrame. Statistic will be created based on this DataFrame.
            async _main_action(df, user_idn):
                Asynchronous function that run coroutines described above.
                parameters:
                    df: DataFrame that will be passed into coroutines.
                    user: unique identifier of user that will be passed into coroutines.
    """

    def get(self, request, idn):
        if 'user' not in request.session:
            cleared_messages(request)
            messages.error(request, 'You are not login yet.')
            return HttpResponseRedirect('/login')

        user_requests = UsersActions.objects.filter(user__identifier=idn)

        if not user_requests:
            return render(request, 'user_statistic/user_stat.html', {'idn': idn, 'statistic': {}})

        stat = {
            'animals': [],
            'disease': [],
            'req_date': []
        }

        for inst in user_requests:
            stat['animals'].append(inst.animal)
            stat['disease'].append(inst.result)
            stat['req_date'].append(inst.prediction_date)

        user_df = pd.DataFrame(stat, columns=[k for k in stat.keys()])

        statistic = asyncio.run(self._main_action(user_df, idn))
        return render(request, 'user_statistic/user_stat.html', {'statistic': statistic, 'idn': idn})


    @staticmethod
    async def _plot_create(df, user):
        fig, ax = plt.subplots(figsize=(12, 10))

        group = df['animals'].value_counts()
        container = ax.bar(group.index, group.values, color=[c for c in 'bgrcmyk'])
        ax.bar_label(container, labels=group.values, padding=2, fontsize=14, weight='bold')

        ax.set_yticks([y for y in range(max(group.values) + 6)] if max(group.values) < 10 else [y for y in range(0, max(group.values) + 11, 10)])
        ax.set_xticks(group.index)

        plt.xlabel('Animals', fontsize=16, fontweight='bold', labelpad=28.0)
        plt.ylabel('Count', fontsize=16, fontweight='bold', labelpad=28.0)
        plt.xticks(fontsize=14, weight='bold')
        plt.yticks(fontsize=14, weight='bold')

        plt.savefig(f'user_statistic/static/images/user_{user}_statistic.png')


    @staticmethod
    async def _create_statistic(df):
        statistic = {
            'request_quantity': df.shape[0],
            'most_freq_animal': df['animals'].value_counts().sort_values(ascending=False).index[0],
            'most_freq_disease': df['disease'].value_counts().sort_values(ascending=False).index[0],
            'last_animal': df['animals'].iloc[-1],
            'last_disease': df['disease'].iloc[-1],
            'last_request_date': df['req_date'].iloc[-1].strftime('%d %B %Y, %H:%M:%S'),
        }
        return statistic


    async def _main_action(self, df, user_idn):
        task_1 = asyncio.create_task(self._plot_create(df, user_idn))
        task_2 = asyncio.create_task(self._create_statistic(df))
        await task_1
        stat = await task_2
        return stat