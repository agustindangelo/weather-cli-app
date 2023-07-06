import requests
import pandas as pd
import numpy as np
import click
import datetime
from datetime import datetime, date
from rich.console import Console
from rich.table import Table
from rich.text import Text

ROS_LATITUDE = -32.95
ROS_LONGITUDE = -60.64
base_url = 'https://api.open-meteo.com/v1/forecast'
console = Console()

def read_weather_codes():
  wc = pd.read_csv('weather-codes.csv')
  wc['Code'] = wc['Code'].apply(lambda string: string.split(','))
  wc['Code'] = wc['Code'].apply(lambda arr: [int(element) for element in arr])

wc = read_weather_codes()

# @click.command()
# @click.option('--days', default=1, help='The forecast time-window')
# @click.option('--output', default='./', help='')
# @click.option('--generate-pdf', default=True, help='Whether to generate a PDF containing all barcodes or not')
# def get_forecast_today():
#   # console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")
#   query_params = {
#     'latitude': ROS_LATITUDE,
#     'longitude': ROS_LONGITUDE,
#     'daily': 'weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_hours,precipitation_probability_max',
#     'current_weather': True,
#     'timezone': 'America/Sao_Paulo',
#     'forecast_days': 1
#   }

#   res = requests.get(base_url, params = query_params).json()
#   console.log(res)
#   return

@click.command()
@click.option('--forecast', default=0, help='The time window to forecast (in days)')
def get_weather(forecast):
  if forecast == 0:
    get_current_weather()
  else:
    get_forecast(forecast)

def get_forecast(forecast):
  console.print('feature not supported')
  
def get_current_weather():
  base_url = 'https://api.open-meteo.com/v1/forecast'
  query_params = {
    'latitude': ROS_LATITUDE,
    'longitude': ROS_LONGITUDE,
    'current_weather': True,
    'timezone': 'America/Sao_Paulo',
  }

  res = requests.get(base_url, params = query_params).json()
  current_weather = res["current_weather"]
  print_current_weather(current_weather)

def print_current_weather(current_weather):
  table = Table(title='Current Weather Conditions')
  table.add_column('Parameter', justify = 'center', header_style="bold magenta", no_wrap = True)
  table.add_column('Value', justify = 'right', header_style = 'bold magenta', no_wrap = True)

  table.add_row('General Condition', get_weather_code_interpretation(current_weather['weathercode']))
  table.add_row('Temperature', str(current_weather['temperature']))
  table.add_row('Wind Speed', str(current_weather['windspeed']))
  table.add_row('Wind Direction', str(current_weather['winddirection']))

  greeting = Text(f'Hi there! Here are the current weather conditions')
  greeting.stylize("bold magenta")

  now = datetime.now()
  current_datetime = Text(now.strftime('%A %B %d, %H%M'))
  current_datetime.stylize("bold magenta")

  console.print(greeting)
  console.print(current_datetime)
  console.print(table)

def get_weather_code_interpretation(weather_code: int):
  wc = pd.read_csv('weather-codes.csv')
  wc['Code'] = wc['Code'].apply(lambda string: string.split(','))
  wc['Code'] = wc['Code'].apply(lambda arr: [int(element) for element in arr])
  msk = wc['Code'].apply(lambda x: weather_code in x)
  return wc.loc[msk, 'Description'].values[0]

if __name__ == '__main__':
  # with console.status("Retrieving forecast...", spinner="aesthetic"):
  # get_forecast_today()
  get_weather()