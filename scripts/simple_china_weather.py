#!/usr/bin/env python3
"""
Simplified China Weather Query - Mimics original weather skill style
"""

import sys
import urllib.parse
import subprocess
import json
import requests

def get_coordinates(location):
    """
    Get coordinates for a location using OpenStreetMap
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location)}&format=json&limit=1"
        response = requests.get(url, headers={'User-Agent': 'Clawbot-China-Weather'})
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
    except:
        pass
    return None, None

def query_opentempero(lat, lon):
    """
    Query Open-Meteo service using coordinates
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius&windspeed_unit=kmh"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current = data['current_weather']
            
            temp = current['temperature']
            weathercode = current['weathercode']
            windspeed = current['windspeed']
            
            # Weather code mapping
            weather_map = {
                0: '晴', 1: '晴间多云', 2: '阴', 3: '阴',
                45: '雾', 48: '雾', 51: '小雨', 53: '中雨', 55: '大雨',
                61: '小雨', 63: '中雨', 65: '大雨', 71: '小雪', 73: '中雪', 75: '大雪',
                95: '雷暴', 96: '雷暴伴冰雹', 99: '雷暴伴大冰雹'
            }
            
            weather_desc = weather_map.get(weathercode, '天气')
            
            return f"{sys.argv[1]}: {weather_desc} {temp}°C 风速:{windspeed}km/h"
    except Exception as e:
        print(f"Error querying Open-Meteo: {e}", file=sys.stderr)
    
    return None

def query_wttr_in(location):
    """
    Query wttr.in service
    """
    try:
        cmd = f'curl -s "wttr.in/{location}?format=3"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            # Translate common weather terms
            translations = {
                'Clear': '晴', 'Sunny': '晴', 'Partly cloudy': '多云', 
                'Cloudy': '多云', 'Overcast': '阴', 'Rain': '雨',
                'Light rain': '小雨', 'Moderate rain': '中雨', 'Heavy rain': '大雨',
                'Showers': '阵雨', 'Snow': '雪', 'Light snow': '小雪',
                'Moderate snow': '中雪', 'Heavy snow': '大雪', 'Fog': '雾',
                'Thunderstorm': '雷暴', 'Thunder': '雷'
            }
            
            for eng, chi in translations.items():
                output = output.replace(eng, chi)
            
            return output
    except Exception as e:
        print(f"Error querying wttr.in: {e}", file=sys.stderr)
    
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_china_weather.py <location>")
        print("Example: python simple_china_weather.py 北京")
        print("Example: python simple_china_weather.py 上海")
        return 1
    
    location = sys.argv[1]
    print(f"Querying weather for: {location}")
    
    # First try wttr.in
    result = query_wttr_in(location)
    if result:
        print(f"Using wttr.in: {result}")
        return 0
    
    # Then try getting coordinates and using Open-Meteo
    print("Trying Open-Meteo...")
    lat, lon = get_coordinates(location)
    if lat and lon:
        result = query_opentempero(lat, lon)
        if result:
            print(f"Using Open-Meteo: {result}")
            return 0
    
    print(f"Could not retrieve weather for: {location}")
    return 1

if __name__ == "__main__":
    sys.exit(main())