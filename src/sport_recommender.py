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
        self.forecast = None
    
    #Function to precompute list of sports for every possible weather forecast    
    def _build_recommendation_dict(self):
        
        #Extract the sport-weather masterlist
        self.sports_df = pd.read_csv(parentdir + '/data/weather-sport-master-list.csv', encoding='latin1')
        
        #Compute the list of recommended sports fore every possible forecast
        self.recommendation_dict = {}
        
        #If rainy, recommend indoor sports
        self.recommendation_dict['Indoor'] = list(self.sports_df[self.sports_df['Indoor']==1]['Sport Id'])
        self.recommendation_dict['Indoor'].sort()
        
        #really warm weather
        self.recommendation_dict['30 or above'] = list(self.sports_df[self.sports_df['30 or above']==1]['Sport Id'])
        self.recommendation_dict['30 or above'].sort()
    
        #warm weather
        self.recommendation_dict['20 to 30'] = list(self.sports_df[self.sports_df['20 to 30']==1]['Sport Id'])
        self.recommendation_dict['20 to 30'].sort()
        
        #comfortable weather
        self.recommendation_dict['10 to 20'] = list(self.sports_df[self.sports_df['10 to 20']==1]['Sport Id'])
        self.recommendation_dict['10 to 20'].sort()
        
        #chilly weather
        self.recommendation_dict['0 to 10'] = list(self.sports_df[self.sports_df['0 to 10']==1]['Sport Id'])
        self.recommendation_dict['0 to 10'].sort()
        
        #cold weather
        self.recommendation_dict['Below 0'] = list(self.sports_df[self.sports_df['Below 0']==1]['Sport Id'])
        self.recommendation_dict['Below 0'].sort() 
        
        
    def get_recommendations(self, lat=45.523, lng=-73.581, days=4, build_recommendation_dict=True):
        
        if build_recommendation_dict:
            self._build_recommendation_dict()
        
        #Get the weather forecast
        wfc = weather_forecaster()
        wfc.get_forecast(lat=lat, lng=lng, days=4)
        self.weather = wfc.forecast
        
        #Filter the list of sports given the predicted weather
        #If rainy, recommend indoor sports
        if self.weather[1] == 1:
            self.recommendation = self.recommendation_dict['Indoor']
            self.forecast = "Mostly rainy forecast"
            
        else:
            #really warm weather
            if self.weather[0] >= 30:
                self.recommendation = self.recommendation_dict['30 or above']
                self.forecast = "Really warm temperature (above 30 Celsius), generally not rainy"
            
            #warm weather
            elif self.weather[0] >= 20:
                self.recommendation = self.recommendation_dict['20 to 30']
                self.forecast = "Warm temperature (between 20 and 30 Celsius), generally not rainy"
                
            #comfortable weather
            elif self.weather[0] >= 10:
                self.recommendation = self.recommendation_dict['10 to 20']
                self.forecast = "Comfortable temperature (between 10 and 20 Celsius), generally not rainy"
                
            #chilly weather
            elif self.weather[0] >= 0:
                self.recommendation = self.recommendation_dict['0 to 10']
                self.forecast = "Chilly temperature (between 0 and 10 Celsius), generally not rainy"
                
            #cold weather
            else:
                self.recommendation = self.recommendation_dict['Below 0']
                self.forecast = "Cold temperature (below 0 Celsius), generally not rainy"
    
    
if __name__ == '__main__':
    rec = sport_recommender()
    rec.get_recommendations()
    
        
        