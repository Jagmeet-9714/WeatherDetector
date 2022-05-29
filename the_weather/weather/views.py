import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e9035c3328892102ceb115ea813c99a5'

    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()

            if existing_city_count==0:
                r = requests.get(url.format(new_city)).json()


                if r['cod']==200:
                    form.save()
                else:
                    err_msg='City Does Not exist in the world !!'

            else:
                err_msg="City already exist in database !!"
    # print(err_msg)

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City Added Successfully'
            message_class = "is-sucess"


    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        temp = r['main']['temp']
        temp1 = (5 / 9) * (temp - 32)
        temp1 = int(temp1)
        city_weather = {
            'city': city.name,
            'temperaturef': temp,
            'temperaturec': temp1,
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

    weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message' : message,
        'message_class' : message_class
    }
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

