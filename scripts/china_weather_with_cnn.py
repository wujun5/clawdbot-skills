#!/usr/bin/env python3
"""
增强版中国天气查询脚本
集成中国天气网API
"""

import requests
import json
import sys
import urllib.parse
import re
from typing import Optional

# 从文件加载中国天气网城市代码
import os
import json

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
city_codes_file = os.path.join(script_dir, 'complete_china_weather_city_codes.json')

try:
    with open(city_codes_file, 'r', encoding='utf-8') as f:
        CITY_CODES = json.load(f)
except FileNotFoundError:
    # 如果文件不存在，使用原始的小型字典作为备用
    CITY_CODES = {
        "北京": "101010100",
        "上海": "101020100",
        "广州": "101280101",
        "深圳": "101280601",
        "杭州": "101210101",
        "南京": "101190101",
        "武汉": "101200101",
        "成都": "101270101",
        "重庆": "101040100",
        "西安": "101110101",
        "天津": "101030100",
        "苏州": "101190401",
        "青岛": "101120201",
        "大连": "101070201",
        "厦门": "101230201",
        "宁波": "101210401",
        "长沙": "101250101",
        "郑州": "101180101",
        "济南": "101120101",
        "福州": "101230101",
        "南昌": "101240101",
        "沈阳": "101060101",
        "哈尔滨": "101050101",
        "石家庄": "101090101",
        "太原": "101100101",
        "昆明": "101290101",
        "南宁": "101300101",
        "合肥": "101220101",
        "海口": "101310101",
        "兰州": "101160101",
        "银川": "101170101",
        "西宁": "101150101",
        "拉萨": "101140101",
        "乌鲁木齐": "101130101",
        "呼和浩特": "101080101",
        "长春": "101060201",
        "唐山": "101090301",
        "秦皇岛": "101091101",
        "邯郸": "101090402",
        "保定": "101090201",
        "张家口": "101090301",
        "承德": "101090402",
        "沧州": "101090701",
        "廊坊": "101090601",
        "衡水": "101090801",
        "邢台": "101090901",
        "晋城": "101100601",
        "朔州": "101100901",
        "忻州": "101101001",
        "大同": "101100201",
        "阳泉": "101100301",
        "长治": "101100501",
        "临汾": "101100701",
        "吕梁": "101101100",
        "运城": "101100801",
        "鞍山": "101070101",
        "抚顺": "101070101",
        "本溪": "101070101",
        "丹东": "101070201",
        "锦州": "101070101",
        "营口": "101070201",
        "阜新": "101070101",
        "辽阳": "101070101",
        "盘锦": "101070401",
        "铁岭": "101070201",
        "朝阳": "101070101",
        "葫芦岛": "101070101",
        "吉林": "101060301",
        "四平": "101060201",
        "辽源": "101060201",
        "通化": "101060501",
        "白山": "101060901",
        "松原": "101060701",
        "白城": "101060601",
        "延边": "101060801",
        "齐齐哈尔": "101050201",
        "鸡西": "101050301",
        "鹤岗": "101050301",
        "双鸭山": "101050301",
        "大庆": "101050901",
        "伊春": "101050801",
        "牡丹江": "101050301",
        "佳木斯": "101050401",
        "七台河": "101050301",
        "黑河": "101050601",
        "绥化": "101050501",
        "大兴安岭": "101050701"
    }

def query_weather_com_cn(city_name: str) -> Optional[str]:
    """
    查询中国天气网API
    """
    # 尝试从城市名获取城市代码
    city_code = CITY_CODES.get(city_name)
    if not city_code:
        # 如果城市名不在预定义列表中，尝试查找包含该名称的条目
        for name, code in CITY_CODES.items():
            if city_name in name or name in city_name:
                city_code = code
                break
    
    if not city_code:
        return None
    
    try:
        # 使用中国天气网的实时天气API
        url = f"http://d1.weather.com.cn/sk_2d/{city_code}.html"
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 解码响应内容（可能是GBK编码）
            try:
                content = response.content.decode('utf-8')
            except UnicodeDecodeError:
                content = response.content.decode('gbk')
            
            # 查找天气信息
            # 中国天气网API返回JavaScript格式的数据
            import re
            # 提取weatherinfo对象
            match = re.search(r'var\s+weatherinfo\s*=\s*({.*?});', content)
            if match:
                json_str = match.group(1)
                # 修复可能的JavaScript特殊字符
                json_str = json_str.replace("'", '"')
                try:
                    data = json.loads(json_str)
                    
                    # 提取天气信息
                    city = data.get('city', city_name)
                    temp = data.get('temp', '未知')
                    wd = data.get('WD', '未知')  # 风向
                    ws = data.get('WS', '未知')  # 风力
                    sd = data.get('SD', '未知')  # 湿度
                    time = data.get('time', '未知')  # 更新时间
                    
                    return f"{city}: {temp}°C 风向:{wd} 风力:{ws} 湿度:{sd} 更新时间:{time}"
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试其他方法
                    pass
            
            # 如果JavaScript解析失败，尝试直接搜索关键信息
            temp_match = re.search(r'"temp":"([^"]*)"', content)
            weather_match = re.search(r'"weather":"([^"]*)"', content)
            
            if temp_match:
                temp = temp_match.group(1)
                weather = weather_match.group(1) if weather_match else "天气"
                return f"{city_name}: {weather} {temp}°C"
        
        return None
    except Exception as e:
        print(f"查询中国天气网API出错: {e}", file=sys.stderr)
        return None

def query_wttr_in(location: str) -> Optional[str]:
    """
    查询wttr.in服务（备用）
    """
    try:
        import subprocess
        cmd = f'curl -s "wttr.in/{location}?format=3"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            # 简单翻译
            translations = {
                'Clear': '晴', 'Sunny': '晴', 'Partly cloudy': '多云', 
                'Cloudy': '阴', 'Overcast': '阴', 'Rain': '雨',
                'Light rain': '小雨', 'Moderate rain': '中雨', 'Heavy rain': '大雨',
                'Showers': '阵雨', 'Snow': '雪', 'Light snow': '小雪',
                'Moderate snow': '中雪', 'Heavy snow': '大雪', 'Fog': '雾',
                'Thunderstorm': '雷暴'
            }
            
            for eng, chi in translations.items():
                output = output.replace(eng, chi)
            
            return output
    except Exception:
        pass
    return None

def query_opentempero_by_city(city_name: str) -> Optional[str]:
    """
    通过城市名使用Open-Meteo服务（需要先获取坐标）
    """
    try:
        # 先获取坐标
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city_name)}&format=json&limit=1"
        response = requests.get(geocode_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Clawbot Weather)'})
        
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            lat = float(data['lat'])
            lon = float(data['lon'])
            
            # 查询天气
            meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius&windspeed_unit=kmh"
            weather_response = requests.get(meteo_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                current = weather_data['current_weather']
                
                temp = current['temperature']
                weathercode = current.get('weathercode', 0)
                windspeed = current['windspeed']
                
                # 天气代码映射
                weather_map = {
                    0: '晴', 1: '晴间多云', 2: '阴', 3: '阴',
                    45: '雾', 48: '雾', 51: '小雨', 53: '中雨', 55: '大雨',
                    61: '小雨', 63: '中雨', 65: '大雨', 71: '小雪', 73: '中雪', 75: '大雪',
                    95: '雷暴', 96: '雷暴伴冰雹', 99: '雷暴伴大冰雹'
                }
                
                desc = weather_map.get(weathercode, '天气')
                
                return f"{city_name}: {desc} {temp}°C 风速:{windspeed}km/h"
    except Exception as e:
        print(f"Open-Meteo查询失败: {e}", file=sys.stderr)
    
    return None

def query_china_weather(location: str) -> str:
    """
    综合查询中国天气
    """
    print(f"正在查询: {location}")
    
    # 1. 首先尝试中国天气网API
    result = query_weather_com_cn(location)
    if result:
        print("使用中国天气网服务")
        return result
    
    # 2. 尝试wttr.in
    result = query_wttr_in(location)
    if result:
        print("使用wttr.in服务")
        return result
    
    # 3. 尝试Open-Meteo
    result = query_opentempero_by_city(location)
    if result:
        print("使用Open-Meteo服务")
        return result
    
    return f"无法获取 {location} 的天气信息"

def main():
    if len(sys.argv) < 2:
        print("使用方法: python china_weather_with_cnn.py <城市名称>")
        print("示例: python china_weather_with_cnn.py 北京")
        print("示例: python china_weather_with_cnn.py 上海")
        return
    
    location = sys.argv[1]
    result = query_china_weather(location)
    print(result)

if __name__ == "__main__":
    main()