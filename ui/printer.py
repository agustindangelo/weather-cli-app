import datetime
import os
from datetime import datetime, date, timedelta
from rich.table import Table
from rich.padding import Padding

def print_forecast(forecast, forecast_days, console):
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


def print_current_weather(current_weather, console):
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
  base_path = os.path.realpath(os.path.dirname(__file__))
  weather_codes_file_name = 'weather-codes.csv'
  weather_codes_file_path = os.path.join(base_path, weather_codes_file_name)

  wc = pd.read_csv(weather_codes_file_path)
  wc['Code'] = wc['Code'].apply(lambda string: string.split(','))
  wc['Code'] = wc['Code'].apply(lambda arr: [int(element) for element in arr])
  msk = wc['Code'].apply(lambda x: weather_code in x)
  return wc.loc[msk, 'Description'].values[0]
