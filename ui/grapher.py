from uniplot import plot
from rich.padding import Padding
from rich.console import Console

console = Console()

def graph_forecast(forecast, forecast_days):
  plot(
    ys = [forecast['temperature_2m_max'], forecast['temperature_2m_min']],
    legend_labels = ['Max. Temperature', 'Min. Temperature'],
    lines = True,
    height = 15,
    x_gridlines = [x for x in range(forecast_days)],
    title=f"Max. & Min. Temperatures for the following {forecast_days} days",
    y_unit="°C"
  )

  padding = Padding("", (1, 0), expand=True)
  console.print(padding)

  plot(
    ys = [forecast['apparent_temperature_max'], forecast['apparent_temperature_min']],
    legend_labels = ['Max. Apparent Temperature', 'Min. Apparent Temperature'],
    lines = True,
    height = 15,
    x_gridlines = [x for x in range(forecast_days)],
    title=f"Max. & Min. Apparent Temperatures for the following {forecast_days} days",
    y_unit="°C"
  )

  console.print(padding)

  plot(
    ys = forecast['precipitation_sum'],
    lines = False,
    color = True,
    height = 14,
    x_gridlines = [x for x in range(forecast_days)],
    title=f"Precipitations {forecast_days} days",
    y_unit="mm"
  )