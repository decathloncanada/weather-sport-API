# -*- coding: utf-8 -*-
"""
Router for the endpoint of the weather-sport-recommendation API

exemple of local url: 
    http://localhost:5000/weather-sport-API?origin=-73.582,45.511&days=4

@author: AI team
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from src import sport_recommender

app = Flask(__name__)
CORS(app)

#function to precompute the recommendations for each possible forecast at the launch
#of the server
def precompute_recommendations():
    global rec
    print('calculated rec')
    rec = sport_recommender.sport_recommender()
    rec._build_recommendation_dict()
    

@app.route('/weather-sport-API')
def get_recommendations():
    #get the lng and lat coordinates for the recommendation
    origin = [float(i) for i in request.args.get('origin').split(',')]    
    
    #get the number of days over witch we want the forecast
    days = int(request.args.get('days'))
    if days > 4:
        days = 4
        print('Number of days has to be between 1 and 4. Set to 4')
        
    elif days < 1:
        days = 1
        print('Number of days has to be between 1 and 4. Set to 0')
    print('fetching calls')
    #call the recommendation system
    rec.get_recommendations(lat=origin[1], lng=origin[0], days=days,
                            build_recommendation_dict=False)
    
    #return recommendations as a json   
    return jsonify({'Sports recommended': rec.recommendation,
                    'Forecast': rec.forecast})

    
if __name__ == '__main__':
    #precompute all recommendations
    precompute_recommendations()
    print('reco computated')
    #run the app
    app.run()
