from datetime import datetime, timedelta
from pyowm import OWM
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/weather")
def weather():
    owm = OWM('11147dbcb05eef551c9357d6a878d33f')
    city = request.args.get("q")
    forecast = owm.three_hours_forecast(city)
    weather = forecast.get_forecast().get_weathers()[0]
    tempreture = weather.get_temperature(unit='celsius')["temp"]

    factors = [ [forecast.will_have_clear(), 0],
                [forecast.will_have_clouds(), 0],
                [forecast.will_have_fog(), -0.1],
                [forecast.will_have_rain(), -0.7 if tempreture < 0 else -0.3],
                [forecast.will_have_snow(),-0.4],
                [forecast.will_have_storm(),-0.5],
                [forecast.will_have_tornado(),-0.5],
                [forecast.will_have_hurricane(),-1]
    ]

    score = 1;
    for factor, value in factors:
        if factor:
            score = score + value
    if score < 0:
        score = 0
    score = score*100


    if score >= 80:
        messege = "Enjoy your Ride"
    elif 60 <= score < 80:
        messege = "Take Care"
    elif 30 <= score < 60:
        messege = "Take caution"
    elif score == 0:
        messege = "DONT DRIVE, Unless you want to die"
    else:
        messege = "Driving is dangerious"



    return jsonify({
        "name": city,
        "drivability_score": score,
        "weather_type": weather.get_status(),
        "icon_url": weather.get_weather_icon_url(),
        "temprature": tempreture,
        "recommendation": messege
    })

@app.route("/home")
def home():
    return "Home Page"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
