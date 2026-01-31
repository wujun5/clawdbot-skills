#!/usr/bin/env python3
"""
增强版中国天气查询模块
支持更多免费API服务，包括无需API密钥的服务
"""

import json
import os
import sys
import urllib.parse
import requests
from datetime import datetime
import time

class EnhancedChinaWeather:
    def __init__(self):
        self.qweather_key = os.environ.get('QWEATHER_API_KEY')
        self.amap_key = os.environ.get('AMAP_API_KEY')
        
    def get_location_coords(self, location):
        """
        通过高德地图API获取坐标，如果无API密钥则使用OpenStreetMap
        """
        if self.amap_key:
            # 使用高德地图API
            try:
                geocode_url = f"https://restapi.amap.com/v3/geocode/geo?key={self.amap_key}&address={urllib.parse.quote(location)}"
                response = requests.get(geocode_url)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == '1' and data.get('geocodes'):
                        location_str = data['geocodes'][0]['location']
                        lon, lat = location_str.split(',')
                        return float(lat), float(lon)
            except:
                pass
        
        # 如果没有高德API密钥或高德失败，使用OpenStreetMap
        try:
            geocode_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location)}&format=json&addressdetails=1&limit=1"
            response = requests.get(geocode_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Clawbot Weather)'})
            
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                return float(data['lat']), float(data['lon'])
        except:
            pass
        return None, None

    def query_apibrew_weather(self, location):
        """
        尝试使用免费的API聚合服务
        这里我们模拟使用一个API聚合服务
        """
        # 这是一个示例，实际中我们会使用真实的免费API
        try:
            # 首先获取坐标
            lat, lon = self.get_location_coords(location)
            if not lat or not lon:
                return None
                
            # 尝试一些免费的天气API
            # 示例：wttr.in (无需API密钥)
            cmd = f'curl -s "wttr.in/{location}?format=3"'
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                # 简单的英文天气描述翻译
                translations = {
                    'Clear': '晴', 'Sunny': '晴', 'Partly cloudy': '多云', 
                    'Cloudy': '阴', 'Overcast': '阴', 'Rain': '雨',
                    'Light rain': '小雨', 'Moderate rain': '中雨', 'Heavy rain': '大雨',
                    'Showers': '阵雨', 'Snow': '雪', 'Light snow': '小雪',
                    'Moderate snow': '中雪', 'Heavy snow': '大雪', 'Fog': '雾',
                    'Thunderstorm': '雷暴'
                }
                
                # 检查是否包含英文描述，如果有则翻译
                for eng, chi in translations.items():
                    output = output.replace(eng, chi)
                
                return output
        except:
            pass
        return None

    def query_weather_api_boxes(self, location):
        """
        模拟API盒子类服务的查询
        这里我们将实现一些真正的免费API
        """
        try:
            # 尝试使用Open-Meteo (无需API密钥)
            lat, lon = self.get_location_coords(location)
            if not lat or not lon:
                return None
            
            meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius&windspeed_unit=kmh&precipitation_unit=mm"
            response = requests.get(meteo_url)
            
            if response.status_code == 200:
                weather_data = response.json()
                current = weather_data['current_weather']
                
                temp = current['temperature']
                windspeed = current['windspeed']
                wind_direction = current['winddirection']
                weathercode = current.get('weathercode', 0)
                
                # 天气代码映射
                weather_map = {
                    0: '晴', 1: '晴间多云', 2: '阴', 3: '阴',
                    45: '雾', 48: '雾', 51: '小雨', 53: '中雨', 55: '大雨',
                    61: '小雨', 63: '中雨', 65: '大雨', 71: '小雪', 73: '中雪', 75: '大雪',
                    95: '雷暴', 96: '雷暴伴冰雹', 99: '雷暴伴大冰雹'
                }
                
                desc = weather_map.get(weathercode, '天气')
                
                result = f"{location}: {desc} {temp}°C 风速:{windspeed}km/h"
                return result
        except Exception as e:
            print(f"Open-Meteo查询失败: {e}", file=sys.stderr)
        
        return None

    def query_chinese_free_api(self, location):
        """
        尝试使用一些中文免费API
        """
        try:
            # 尝试使用一些免费的天气API服务
            # 使用OpenWeatherMap的免费层级（需要API密钥，但提供示例）
            # 这里我们只列出可用的API，实际使用需要用户自己的密钥
            pass
        except:
            pass
        return None

    def query_weather(self, location):
        """
        查询天气信息，按优先级尝试不同服务
        更新后的优先级包括更多免费选项
        """
        print(f"正在查询 {location} 的天气信息...")
        
        # 1. 尝试和风天气 (如果有API密钥)
        if self.qweather_key:
            result = self.query_qweather(location)
            if result:
                print("使用和风天气服务")
                return result
        
        # 2. 尝试高德地图天气 (如果有API密钥)
        if self.amap_key:
            result = self.query_amap_weather(location)
            if result:
                print("使用高德地图天气服务")
                return result
        
        # 3. 尝试Open-Meteo (无需API密钥)
        result = self.query_weather_api_boxes(location)
        if result:
            print("使用Open-Meteo服务")
            return result
        
        # 4. 尝试wttr.in (无需API密钥)
        result = self.query_apibrew_weather(location)
        if result:
            print("使用wttr.in服务")
            return result
        
        # 5. 尝试其他免费服务
        result = self.query_chinese_free_api(location)
        if result:
            print("使用中文免费API服务")
            return result
        
        return f"无法获取 {location} 的天气信息"

    def query_qweather(self, location):
        """和风天气查询实现"""
        if not self.qweather_key:
            return None
            
        try:
            # 先获取地理坐标
            lat, lon = self.get_location_coords(location)
            if not lat or not lon:
                # 尝试直接使用地点名称
                search_url = f"https://geoapi.qweather.com/v2/city/lookup?location={urllib.parse.quote(location)}&key={self.qweather_key}"
                search_resp = requests.get(search_url)
                if search_resp.status_code == 200:
                    search_data = search_resp.json()
                    if search_data.get('code') == '200' and search_data.get('location'):
                        location_id = search_data['location'][0]['id']
                    else:
                        return None
                else:
                    return None
            else:
                # 使用坐标查询天气
                weather_url = f"https://devapi.qweather.com/v7/weather/now?location={lon},{lat}&key={self.qweather_key}"
            response = requests.get(weather_url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '200':
                    now = data['now']
                    temp = now['temp']
                    text = now['text']
                    wind_dir = now['windDir']
                    wind_scale = now['windScale']
                    
                    result = f"{location}: {text} {temp}°C 风向:{wind_dir} 风力:{wind_scale}级"
                    return result
        except Exception as e:
            print(f"QWeather查询失败: {e}", file=sys.stderr)
        
        return None
    
    def query_amap_weather(self, location):
        """高德地图天气查询实现"""
        if not self.amap_key:
            return None
            
        try:
            # 先获取城市编码
            city_url = f"https://restapi.amap.com/v3/config/district?keywords={urllib.parse.quote(location)}&subdistrict=0&key={self.amap_key}"
            city_resp = requests.get(city_url)
            
            if city_resp.status_code == 200:
                city_data = city_resp.json()
                if city_data.get('status') == '1' and city_data.get('districts'):
                    city_code = city_data['districts'][0]['citycode']
                    
                    # 查询天气
                    weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={self.amap_key}&extensions=base"
                    weather_resp = requests.get(weather_url)
                    
                    if weather_resp.status_code == 200:
                        weather_data = weather_resp.json()
                        if weather_data.get('status') == '1' and weather_data.get('lives'):
                            live = weather_data['lives'][0]
                            weather = live['weather']
                            temperature = live['temperature']
                            wind_direction = live['winddirection']
                            wind_power = live['windpower']
                            
                            result = f"{location}: {weather} {temperature}°C 风向:{wind_direction} 风力:{wind_power}级"
                            return result
        except Exception as e:
            print(f"AMap天气查询失败: {e}", file=sys.stderr)
        
        return None


def main():
    if len(sys.argv) < 2:
        print("用法: python enhanced_query_china_weather.py <城市名称>")
        print("示例: python enhanced_query_china_weather.py 北京")
        print("示例: python enhanced_query_china_weather.py 上海")
        return
    
    location = " ".join(sys.argv[1:])
    weather = EnhancedChinaWeather()
    result = weather.query_weather(location)
    print(result)


if __name__ == "__main__":
    main()