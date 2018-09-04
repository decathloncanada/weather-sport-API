# -*- coding: utf-8 -*-
"""
Class to extract weather information at a given location.

Input: lat, lng and number of days over which we want the forecast (1-4). Note that
if days=0, we take the current weather.

Output: The average temperature forcasted at 12h and 15h (local time) over the forecasting
period, and if rain is in the forecast or not. The output can be found in the tuple self.forecast,
which contains two elements:
    first element --> average T forecasted
    second element --> 0 if rainy most of the forecast, 1 otherwise

@author: AI team
"""

from datetime import datetime, timedelta
import numpy as np
from pyowm import OWM
from pytz import timezone
import timezonefinder
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

try:
    from config import owm_key
except:
    #grab keys from the environment
    owm_key = os.environ.get('OWM_KEY')
    
   
class weather_forecaster():
    
    def __init__(self):
        self.forecast = None
        
    def get_forecast(self, lat=45.523, lng=-73.581, days=4):
        owm = OWM(owm_key)
        
        self.lat = lat
        self.lng = lng
        self.days = days
        
        #if we want to use current weather
        if days == 0:
            fc = owm.weather_at_coords(self.lat, self.lng)
            w = fc.get_weather()
            self.T = w.get_temperature('celsius')['temp']
            self.rain = 1 if not w.get_rain() else 0
            self.forecast = (self.T, self.rain)
        
        #if we want to use weather forecast
        else:
            #Get weather forecast over the next five days, at 3h intervals
            fc = owm.three_hours_forecast_at_coords(self.lat, self.lng)
            
            #Get tempreature forecast and weather status at 12h and 15h (local time) over the next four days
            #Get the timezone
            tf = timezonefinder.TimezoneFinder()
            timezone_str = tf.certain_timezone_at(lat=self.lat, lng=self.lng)
            
            #Get the current local time
            self.clt = datetime.now()
            
            #Create a list of local times for which we want a forecast
            forecast_wanted = [self.clt + timedelta(days=i) for i in range(1,self.days+1)]
            list_of_forecast_wanted = [i.replace(hour=12) for i in forecast_wanted] + \
            [i.replace(hour=15) for i in forecast_wanted]
                   
            #Change from local time to utc
            tmz = timezone(timezone_str)
            list_of_forecast_wanted = [tmz.localize(i).astimezone(timezone('UTC')) for i in list_of_forecast_wanted]
            
            #Get the temperature forecast and average temperature
            temperature_forecast = [fc.get_weather_at(i).get_temperature('celsius')['temp'] for i in list_of_forecast_wanted]
            self.average_forecasted_T = np.mean(temperature_forecast)
            
            #See if it forecasts rain or not (0-->no rain, 1-->rain)      
            rain_forecast = [1 if fc.will_be_rainy_at(i) else 0 for i in list_of_forecast_wanted]
    
            self.rain = 1 if float(np.sum(rain_forecast))/len(rain_forecast) >= 0.5 else 0
            
            self.forecast = (self.average_forecasted_T, self.rain)

        
if __name__ == '__main__':
    DAYS = 0
    
    wfc = weather_forecaster()
    wfc.get_forecast(days=DAYS)

        
        
