import requests

def get_weather_data(api_key, city):
    url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            weather_info = {
                "aqi": data['data']['aqi'],  # Air Quality Index
                "temperature": data['data']['iaqi'].get('t', {}).get('v', 'N/A'),
                "humidity": data['data']['iaqi'].get('h', {}).get('v', 'N/A')
            }
            return weather_info
    return {"error": "Failed to fetch weather data"}
