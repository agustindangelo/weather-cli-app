# Setup

```
pip install -r ./requirements.txt
```

# Get todays' weather conditions

```powershell
python ./w.py
```

# Forecast up to n days ahead

```powershell
python ./w.py --forecast-days 7
```

## Handy Aliases (Powershell)

```powershell
function get-weather { python C:\Users\adangelo\code\weather\w.py }
function get-forecast7 { python C:\Users\adangelo\code\weather\w.py --forecast-days 7 }
Set-Alias gw get-weather
Set-Alias gf7 get-forecast7
```
