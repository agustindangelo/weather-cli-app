import requests

base_url = 'https://api.open-meteo.com/v1/forecast'
ROS_LATITUDE = -32.95
ROS_LONGITUDE = -60.64

def get_forecast(forecast_days):
  query_params = {
    'latitude': ROS_LATITUDE,
    'longitude': ROS_LONGITUDE,
    'daily': 'weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_hours,precipitation_probability_max',
    'current_weather': True,
    'timezone': 'America/Sao_Paulo',
    'forecast_days': forecast_days
  }

  res = requests.get(base_url, params = query_params).json()

  return res

def get_current_weather():
  query_params = {
    'latitude': ROS_LATITUDE,
    'longitude': ROS_LONGITUDE,
    'current_weather': True,
    'timezone': 'America/Sao_Paulo',
  }

  res = requests.get(base_url, params = query_params).json()
  current_weather = res["current_weather"]
  return current_weather