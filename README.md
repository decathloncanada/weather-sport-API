# weather-sport-API
The API provides the list of sports which can be practiced given the weather forecast. The inputs of the API are the geolocation (lat and lng) of interest and the number of days (from one to four) over which we want to consider the weather weather forecast. The output is the list of sports matching the weather forecast. 

For any additional information, please contact samuel.mercier@decathlon.com

## Algorithm
When the API is called, the weather forecasted at the given location is obtained by calling [pyowm](https://github.com/csparpa/pyowm), a python wrapper around the OpenWeatherMap web API. Two features are then extracted from the forecast, the average temperature at noon and 3 pm (local time) over the forecasting period and whether rain is forecasted at more than half these time steps. The sports are recommended following these general guidelines

| Weather forecast | Sports recommended |
| ------------- |:-------------:|
| Generally rainy  | indoor sports |
| Cold average temperature (< 0 °C), generally not rainy | outdoor winter sports |
| Chilly average temperature (0-10 °C), generally not rainy | outdoor year-long sports (hiking, jogging, etc.)|
| Comfortable average temperature (10-20 °C), generally not rainy | outdoor summer sports, excluding water sports |
| Warm average temperature (20-30 °C), generally not rainy | outdoor summer sports |
| Very warm average temperature (> 30 °C), generally not rainy | outdoor water sports |



