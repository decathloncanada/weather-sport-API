# -*- coding: utf-8 -*-
"""
Class to recommend sports given the weather. 

Input: lat, lng and number of days over which we want the forecast (1-4)

Output: list of recommended sports

The recommended sports is decided given the average max temperature, and the 
number of rainy days.

@author: AI team
"""
import pandas as pd
import os,inspect, sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from src.weather_forecaster import weather_forecaster

class sport_recommender():
    
    def __init__(self):
        self.recommendation = None
        self.reason = None
        
    def get_recommendations(self, lat=45.523, lng=-73.581, days=4):
        
        #Extract the sport-weather masterlist
        self.sports_df = pd.read_csv(parentdir + '/data/weather-sport-master-list.csv', encoding='latin1')

        #Get the weather forecast
        wfc = weather_forecaster()
        wfc.get_forecast(lat=lat, lng=lng, days=4)
        self.forecast = wfc.forecast
        
        #Filter the list of sports given the predicted weather
        #If rainy, recommend indoor sports
        if self.forecast[1] == 1:
            self.recommendation = list(self.sports_df[self.sports_df['Indoor']==1]['Sport Id']).sort()
            self.reason = "Mostly rainy forecast"
            
        else:
            #really warm forecast
            if self.forecast[0] >= 30:
                self.recommendation = list(self.sports_df[self.sports_df['30 or above']==1]['Sport Id'])
                self.recommendation.sort()
                self.reason = "Really warm temperature (above 30 Celsius), mostly not rainy"
            
            #warm forecast
            elif self.forecast[0] >= 20:
                self.recommendation = list(self.sports_df[self.sports_df['10 to 20']==1]['Sport Id'])
                self.recommendation.sort()
                self.reason = "Warm temperature (between 20 and 30 Celsius), mostly not rainy"
                
            #comfortable forecast
            elif self.forecast[0] >= 10:
                self.recommendation = list(self.sports_df[self.sports_df['10 to 20']==1]['Sport Id'])
                self.recommendation.sort()
                self.reason = "Comfortable temperature (between 10 and 20 Celsius), mostly not rainy"
                
            #chilly forecast
            elif self.forecast[0] >= 0:
                self.recommendation = list(self.sports_df[self.sports_df['0 to 10']==1]['Sport Id'])
                self.recommendation.sort()
                self.reason = "Chilly temperature (between 0 and 10 Celsius), mostly not rainy"
                
            #cold forecast
            else:
                self.recommendation = list(self.sports_df[self.sports_df['Below 0']==1]['Sport Id'])
                self.recommendation.sort()
                self.reason = "Cold temperature (below 0 Celsius), mostly not rainy"
        
if __name__ == '__main__':
    rec = sport_recommender()
    rec.get_recommendations()
    
        
        