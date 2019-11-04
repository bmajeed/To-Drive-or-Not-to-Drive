from datetime import datetime, timedelta
from pyowm import OWM


API_key = '11147dbcb05eef551c9357d6a878d33f'
owm = OWM(API_key)
city = 'Andermatt, USA'

forecast = owm.three_hours_forecast(city)
weather = forecast.get_forecast().get_weathers()[0]
tempreture = weather.get_temperature(unit='celsius')["temp"]

print(weather.get_detailed_status())

icon_url = weather.get_weather_icon_url()

factors = [ [forecast.will_have_clear(), 0],
            [forecast.will_have_clouds(), 0],
            [forecast.will_have_fog(),0.1],
            [forecast.will_have_rain(), 0.7 if tempreture < 0 else 0.3],
            [forecast.will_have_snow(),-0.4],
            [forecast.will_have_storm(),-0.5],
            [forecast.will_have_tornado(),-0.5],
            [forecast.will_have_hurricane(),-1]
]

print(factors)

index = 1;
for factor, value in factors:
        if factor:
            index+= value
if index < 0:
    index = 0
index = index*100
print(index)