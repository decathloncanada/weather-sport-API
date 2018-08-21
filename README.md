# weather-sport-API
The API provides the list of sports which can be practiced given the weather forecast. The inputs of the API are the geolocation (lat and lng) of interest and the number of days (one to four) over which we want to consider the weather forecast. The output is the list of sports matching the weather conditions. 

For any additional information, please contact samuel.mercier@decathlon.com

## Algorithm
When the API is called, the weather forecasted at the given location is obtained by calling [pyowm](https://github.com/csparpa/pyowm), a python wrapper around the OpenWeatherMap web API. Two features are then extracted from the forecast, the average temperature at noon and 3 pm (local time) over the forecasting period and whether rain is forecasted at more than half of these time steps. The sports are recommended following these general guidelines

| Weather forecast | Sports recommended |
| ------------- |-------------|
| Generally rainy  | indoor sports |
| Cold temperature (< 0 °C), generally not rainy | outdoor winter sports |
| Chilly temperature (0-10 °C), generally not rainy | outdoor year-long sports (hiking, jogging, etc.)|
| Comfortable temperature (10-20 °C), generally not rainy | outdoor summer sports, excluding water sports |
| Warm temperature (20-30 °C), generally not rainy | outdoor summer sports |
| Very warm temperature (> 30 °C), generally not rainy | outdoor water sports |

The association between the sports and the weather forecast can be found and edited in the ./data/weather-sport-master-list.csv file. Note that a given sport can be found accross a number of forecast ranges (exemple: ice hockey, which is both an indoor sport and an outdoor winter sport).

## Getting started
1. git clone the project to the desired location
```
git clone https://github.com/decathloncanada/weather-sport-API.git
```

2. Make sure you have python 3 installed

3. Install the dependencies:
```
sudo pip install -r requirements.txt
```

4. Add a config.py file, in the root of the project, containing your [OpenWeatherMap API key](https://openweathermap.org/appid). The config.py file should be as follows:
```
owm_key={OWM_KEY}
```
where you replace {OWM_KEY} with your Open Weather Map key.

## API call
To get the sport recommendations at a given location given the weather forecast, run the project as follows:
```
python app.py
```
The API will then be available at http://localhost:5000/weather-sport-API. The API takes two arguments:
  - *origin* : longitude and latitude of the location of interest
  - *days*: the period (number of days) over which we consider the weather forecast. Should be an integer between 1 and 4.
  
The API returns a json containing the ID of the recommended sports and a short description of the weather forecast in a json format.

As an example, here's a call to recommend the sports given the weather forecasted over the next two days at a given location in Montreal:
```
http://localhost:5000/weather-sport-API?origin=-73.582,45.511&days=2
```

The returned json should look like:
```
{"Forecast":"Warm temperature (between 20 and 30 Celsius), generally not rainy","Sports recommended":[12,29,37,45,49,51,74,76,78,81,87,89,98,134,141,143,147,150,163,166,171,178,180,182,186,219,224,280,281,282,283,284,285,286,287,288,289,292,294,296,298,305,306,308,309,310,311,312,318,319,320,321,322,323,324,328,329,330,331,389,392,395,404,409,449,461,466,471,473,487,490]}
```
The information about the sports given their IDs can be obtained from the [Sports API](https://developers.decathlon.com/sportplaces/#sports).

## Roadmap
The next steps of the project will be to sync the API with the updated version of the Sports API, and include informations about the sun, wind and snow conditions to refine the recommendations.
