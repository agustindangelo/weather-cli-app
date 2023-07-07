import requests
import pandas as pd
import numpy as np
import click
import datetime
from uniplot import plot
from datetime import datetime, date, timedelta
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding

ROS_LATITUDE = -32.95
ROS_LONGITUDE = -60.64
base_url = 'https://api.open-meteo.com/v1/forecast'
console = Console()

@click.command()
@click.option('--forecast-days', default=0, help='The time window on which to forecast (in days)')
@click.option('--graph', default=True, help='Whether to generate graphs or not')
def get_weather(forecast_days, graph):
  with console.status("Retrieving forecast...", spinner="aesthetic"):
    if forecast_days == 0:
      get_current_weather()
    else:
      get_forecast(forecast_days, graph)

def get_forecast(forecast_days, graph):
  if forecast_days > 16:
    error = Text('Cannot generate forecasts for more than 16 days ahead. Forecasts will be retrieved for the next 16 days.', justify='center')
    error.stylize("bold red")
    console.print(error)
    forecast_days = 16

  query_params = {
    'latitude': ROS_LATITUDE,
    'longitude': ROS_LONGITUDE,
    'daily': 'weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_hours,precipitation_probability_max',
    'current_weather': True,
    'timezone': 'America/Sao_Paulo',
    'forecast_days': forecast_days
  }

  res = requests.get(base_url, params = query_params).json()
  print_forecast(res['daily'], forecast_days)

  if graph:
    graph_forecast(res['daily'], forecast_days)
  
def get_current_weather():
  query_params = {
    'latitude': ROS_LATITUDE,
    'longitude': ROS_LONGITUDE,
    'current_weather': True,
    'timezone': 'America/Sao_Paulo',
  }

  res = requests.get(base_url, params = query_params).json()
  current_weather = res["current_weather"]
  print_current_weather(current_weather)

def graph_forecast(forecast, forecast_days):
  plot(
    ys = [forecast['temperature_2m_max'], forecast['temperature_2m_min']],
    legend_labels = ['Max. Temperature', 'Min. Temperature'],
    lines = True,
    x_gridlines = [x for x in range(forecast_days)],
    title=f"Max. & Min. Temperatures for the following {forecast_days} days",
    y_unit="°C"
  )

  plot(
    ys = [forecast['apparent_temperature_max'], forecast['apparent_temperature_min']],
    legend_labels = ['Max. Apparent Temperature', 'Min. Apparent Temperature'],
    lines = True,
    x_gridlines = [x for x in range(forecast_days)],
    title=f"Max. & Min. Apparent Temperatures for the following {forecast_days} days",
    y_unit="°C"
  )

  plot(
    ys = forecast['precipitation_sum'],
    lines = True,
    x_gridlines = [x for x in range(forecast_days)],
    title=f"Precipitations {forecast_days} days",
    y_unit="mm"
  )

def print_forecast(forecast, forecast_days):
  table = Table(title=f'Forecast for the following {forecast_days} days', caption='Source: open-meteo.com')

  table.add_column(no_wrap=True)
  for i in range(forecast_days):
    day = date.today() + timedelta(days = i)
    day = day.strftime('%A %d')
    table.add_column(day, justify='right')

  table.add_row('Max. Temperature (°C)', *[str(value) for value in forecast['temperature_2m_max']])
  table.add_row('Min. Temperature (°C)', *[str(value) for value in forecast['temperature_2m_min']])
  table.add_row('Apparent Max. Temperature (°C)', *[str(value) for value in forecast['apparent_temperature_max']])
  table.add_row('Apparent Min. Temperature (°C)', *[str(value) for value in forecast['apparent_temperature_min']])
  table.add_row('Precipitations (mm)', *[str(value) for value in forecast['precipitation_sum']])
  table.add_row('Precipitation Hours (h)', *[str(value) for value in forecast['precipitation_hours']])
  table.add_row('Max. Precipiation Probability (%)', *[str(value) for value in forecast['precipitation_probability_max']])

  padding = Padding("", (1, 0), expand=True)
  console.print(padding)
  console.print(table)
  console.print(padding)


def print_current_weather(current_weather):
  table = Table(title='Current Weather Conditions')
  table.add_column()
  table.add_column('Values', justify = 'right')

  table.add_row('Date Time', datetime.now().strftime('%A %B %d, %H:%M'))
  table.add_row('General Condition', get_weather_code_interpretation(current_weather['weathercode']))
  table.add_row('Temperature', f"{str(current_weather['temperature'])} °C")
  table.add_row('Wind Speed', f"{str(current_weather['windspeed'])} Km/h")
  table.add_row('Wind Direction', f"{str(current_weather['winddirection'])} °")


  padding = Padding("", (1, 0), expand=True)
  console.print(padding)
  console.print(table)
  console.print(padding)

def get_weather_code_interpretation(weather_code: int):
  wc = pd.read_csv('weather-codes.csv')
  wc['Code'] = wc['Code'].apply(lambda string: string.split(','))
  wc['Code'] = wc['Code'].apply(lambda arr: [int(element) for element in arr])
  msk = wc['Code'].apply(lambda x: weather_code in x)
  return wc.loc[msk, 'Description'].values[0]

if __name__ == '__main__':
  get_weather()