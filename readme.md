# Setup

```
pip install -r ./requirements.txt
```

# Get todays' weather conditions

```powershell
python ./w.py
```
![image](https://github.com/agustindangelo/weather-cli-app/assets/52323045/2fb96e7f-1eb2-4d35-bc18-b6f3f0bd8cae)

# Forecast up to n days ahead

```powershell
python ./w.py --forecast-days 7
```
![image](https://github.com/agustindangelo/weather-cli-app/assets/52323045/c85b5bbb-e0aa-4024-a3a0-f4faa557a460)
![image](https://github.com/agustindangelo/weather-cli-app/assets/52323045/6f0509b8-b465-4a70-8471-e7382aec3696)

## Handy Aliases (Powershell)

```powershell
function get-weather { python C:\Users\adangelo\code\weather\w.py }
function get-forecast7 { python C:\Users\adangelo\code\weather\w.py --forecast-days 7 }
Set-Alias gw get-weather
Set-Alias gf7 get-forecast7
```
