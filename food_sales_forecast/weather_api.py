import requests
import datetime
import os

# APIキーと都市設定（例：東京）
API_KEY = os.getenv("WEATHER_API_KEY", "your_openweathermap_api_key")
CITY_ID = 1850147  # 東京の都市ID

# 天気コードのマッピング（晴れ：2、曇：1、雨：0）
def map_weather_to_code(description):
    if "rain" in description.lower():
        return 0
    elif "cloud" in description.lower():
        return 1
    elif "clear" in description.lower():
        return 2
    else:
        return 1  # デフォルト：曇

def fetch_weekly_weather():
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?id={CITY_ID}&cnt=7&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    results = []
    for day in data["list"]:
        weather_desc = day["weather"][0]["main"]
        temp = day["temp"]["day"]
        results.append({
            "weather": weather_desc,
            "code": map_weather_to_code(weather_desc),
            "temp": round(temp, 1)
        })

    return results