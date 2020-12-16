import os
import re
from datetime import date, datetime

import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from .models import Show


class ShowManager():
        
    def is_show(self, pk):
        return Show.objects.filter(pk=pk).first()
        
    def add_new_show(self, pk):
        new_show = Show()
        api_data = self.api_data(pk, None)
        if api_data:
            ''' Check if show is still running '''
            status = api_data.get('status')
            if status == 'Ended' or status == 'Canceled':
                return messages.add_message(
                    self.request, messages.INFO, '<strong>Oops!</strong> - That show is over.'
                )

            new_show.pk = api_data.get('id')
            new_show.name = api_data.get('name')

            ''' check if there is a poster path '''
            poster_path = api_data.get('poster_path')
            if poster_path:
                new_show.poster_path = poster_path
                self.save_poster(poster_path)

            ''' check episode data '''
            episode_data = api_data.get('next_episode_to_air')
            if episode_data:
                new_show.episode_number = episode_data.get('episode_number')
                new_show.season_number = episode_data.get('season_number')
                new_show.episode_name = episode_data.get('name')
                new_show.next_episode_date = datetime.strptime(
                    episode_data.get('air_date'), '%Y-%m-%d').date()

            new_show.save()
            return messages.add_message(
                self.request, messages.SUCCESS, '<strong>Success!</strong> - show added.'
            )

    def update_show(self, show):
        today = date.today()
        api_data = self.api_data(show.id, None)
        if api_data:
            status = api_data.get('status')
            if status == 'Ended' or status == 'Canceled':
                show.delete()
                return messages.add_message(
                    self.request, messages.INFO, '<strong>Oops!</strong> - That show is over.'
                )

            episode_data = api_data.get('next_episode_to_air')
            if episode_data:
                ''' update show next episode dates '''
                show.episode_number = episode_data.get('episode_number')
                show.season_number = episode_data.get('season_number')
                show.episode_name = episode_data.get('name')

                next_apisode = datetime.strptime(episode_data.get('air_date'), '%Y-%m-%d').date()
                if next_apisode >= today:
                    show.next_episode_date = next_apisode
                else:
                    show.next_episode_date = None
            else:
                ''' clear out old episode data if there is no new episodes_data '''
                show.next_episode_date = None
                show.episode_number = None
                show.season_number = None
                show.episode_name = None

            show.save()

    def remove_show(self, show):
        show.delete()
        return messages.add_message(
            self.request, messages.WARNING, f'<strong>removed!</strong> - {show.name}'
        )

    def save_poster(self, path):
        if path:
            fullpath = f'{settings.BASE_DIR}/static/images/posters{path}'
            if not os.path.exists(fullpath):
                url = 'https://image.tmdb.org/t/p/w342' + path
                response = requests.get(url)
                with open(fullpath, 'wb') as f:
                    f.write(response.content)

    def api_data(self, pk, string):
        show_url = f'https://api.themoviedb.org/3/tv/{pk}?api_key={settings.API_KEY}&language=en-US&append_to_response=images'
        search_url = f'https://api.themoviedb.org/3/search/tv?api_key={settings.API_KEY}&language=en-US&page=1&query={str(string)}'
        response = None

        ''' get show data when adding to list '''
        if pk:
            response = requests.get(show_url)

        ''' gets search results data from api '''
        if string:
            response = requests.get(search_url)

        if response.status_code == 200:
            return response.json()
        return False


class ShowListView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Show.objects.order_by('-next_episode_date')


class ShowAddView(View, ShowManager):
    template_name = 'home'

    def get(self, request, *args, **kwargs):
        show = self.is_show(kwargs['pk'])
        if not show:
            self.add_new_show(kwargs['pk'])

        return redirect(self.template_name)


class ShowRemoveView(View, ShowManager):
    template_name = 'home'

    def get(self, request, *args, **kwargs):
        show = self.is_show(kwargs['pk'])
        if show:
            self.remove_show(show)
        return redirect(self.template_name)


class SearchView(View, ShowManager):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        context = {}
        search_str = re.sub(r'[^a-zA-Z0-9\s-]+', '', request.GET.get('search'))
        data = self.search_data(search_str)
        context['data_results'] = data if data else None
        return render(request, self.template_name, context)

    def search_data(self, string):
        id_qry = [i.pk for i in Show.objects.all()]
        results_list = []
        data = self.api_data(None, string)
        if data:
            for i in data['results']:
                exists = True if int(i['id']) in id_qry else False
                l = {
                    'pk': i['id'],
                    'name': i['name'],
                    'image': i['poster_path'],
                    'overview': i['overview'],
                    'popularity': i['popularity'],
                    'exists': exists,
                }
                results_list.append(l)
            return results_list
        return None


