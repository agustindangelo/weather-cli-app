from api.weather_requests import get_current_weather, get_forecast
from ui.grapher import graph_forecast
from ui.printer import print_current_weather, print_forecast
import click

@click.command()
@click.option('--forecast-days', default=0, help='The time window on which to forecast (in days)')
@click.option('--graph', default=True, help='Whether to generate graphs or not')
def get_weather(forecast_days, graph):
  if forecast_days == 0:
    current_weather = get_current_weather()
    print_current_weather(current_weather)

  else:
    forecast = get_forecast(forecast_days)
    print_forecast(forecast, forecast_days)

    if graph:
      graph_forecast(forecast, forecast_days) 

if __name__ == '__main__':
  get_weather()