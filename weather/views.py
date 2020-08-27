from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests

import geocoder
# Create your views here.

def index(request):
    # return render(request, 'weather/index.html')
    current_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4c41700b14cc905839ce79898dbe9a09'

    # city = 'Lubaczów'
    err_msg = 0
    g = geocoder.ip('me')
    user_city = g.city

    if 'city' in request.GET:
        city = request.GET.get('city')

        r = requests.get(current_url.format(city)).json()
        if r['cod'] != 200:
            err_msg = 1
            # r = requests.get(url.format(g.city)).json()
            # city = g.city
        else:
            user_city = city

    r = requests.get(current_url.format(user_city)).json()
    city_weather = {
        'city' : user_city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
        'wind' : r['wind']['speed'],
        'pressure' : r['main']['pressure'],
    }

    form = CityForm()
    context = {'city_weather' : city_weather, 'form' : form, 'err_msg' : err_msg}
    return render(request, 'weather/index'
                           '.html', context)