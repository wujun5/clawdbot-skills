#!/usr/bin/env python3
"""
智能回退版中国天气查询脚本
当无法查询到具体城市时，自动回退到省级或附近城市
"""

import requests
import json
import sys
import urllib.parse
import re
from typing import Optional
import os

def load_city_codes():
    """加载城市代码"""
    # 尝试多个可能的路径
    possible_paths = [
        '/home/Tim/BotRoom/complete_china_weather_city_codes.json',
        '/home/Tim/BotRoom/clawdbot-skills/scripts/complete_china_weather_city_codes.json',
        '/home/Tim/BotRoom/skills_workspace/china-weather/scripts/complete_china_weather_city_codes.json',
        './complete_china_weather_city_codes.json'
    ]

    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    print(f"从 {path} 加载了 {len(json.load(f))} 个城市代码")
                    f.seek(0)  # 重置文件指针
                    return json.load(f)
        except FileNotFoundError:
            continue
    
    # 如果没有找到完整文件，使用备用字典
    backup_codes = {
        "北京": "101010100", "上海": "101020100", "广州": "101280101", "深圳": "101280601",
        "杭州": "101210101", "南京": "101190101", "武汉": "101200101", "成都": "101270101",
        "重庆": "101040100", "西安": "101110101", "天津": "101030100", "苏州": "101190401",
        "青岛": "101120201", "大连": "101070201", "厦门": "101230201", "宁波": "101210401",
        "长沙": "101250101", "郑州": "101180101", "济南": "101120101", "福州": "101230101",
        "南昌": "101240101", "沈阳": "101060101", "哈尔滨": "101050101", "石家庄": "101090101",
        "太原": "101100101", "昆明": "101290101", "南宁": "101300101", "合肥": "101220101",
        "海口": "101310101", "兰州": "101160101", "银川": "101170101", "西宁": "101150101",
        "拉萨": "101140101", "乌鲁木齐": "101130101", "呼和浩特": "101080101", "长春": "101060201",
        "唐山": "101090301", "秦皇岛": "101091101", "邯郸": "101090402", "保定": "101090201",
        "张家口": "101090301", "承德": "101090402", "沧州": "101090701", "廊坊": "101090601",
        "衡水": "101090801", "邢台": "101090901", "晋城": "101100601", "朔州": "101100901",
        "忻州": "101101001", "大同": "101100201", "阳泉": "101100301", "长治": "101100501",
        "临汾": "101100701", "吕梁": "101101100", "运城": "101100801", "鞍山": "101070101",
        "抚顺": "101070101", "本溪": "101070101", "丹东": "101070201", "锦州": "101070101",
        "营口": "101070201", "阜新": "101070101", "辽阳": "101070101", "盘锦": "101070401",
        "铁岭": "101070201", "朝阳": "101070101", "葫芦岛": "101070101", "吉林": "101060301",
        "四平": "101060201", "辽源": "101060201", "通化": "101060501", "白山": "101060901",
        "松原": "101060701", "白城": "101060601", "延边": "101060801", "齐齐哈尔": "101050201",
        "鸡西": "101050301", "鹤岗": "101050301", "双鸭山": "101050301", "大庆": "101050901",
        "伊春": "101050801", "牡丹江": "101050301", "佳木斯": "101050401", "七台河": "101050301",
        "黑河": "101050601", "绥化": "101050501", "大兴安岭": "101050701"
    }
    print("警告: 未能加载完整城市代码文件，使用备用字典")
    return backup_codes

def load_province_codes():
    """加载省份代码"""
    # 尝试多个可能的路径
    possible_paths = [
        '/home/Tim/BotRoom/china_weather_province_codes.json',
        '/home/Tim/BotRoom/clawdbot-skills/scripts/china_weather_province_codes.json',
        '/home/Tim/BotRoom/skills_workspace/china-weather/scripts/china_weather_province_codes.json',
        './china_weather_province_codes.json'
    ]

    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except FileNotFoundError:
            continue
    
    # 如果没有找到省份代码文件，返回空字典
    return {}

def find_city_code(city_name: str, city_codes: dict, province_codes: dict):
    """查找城市代码，支持城市名和省份+城市名的组合"""
    # 首先尝试精确匹配城市名
    if city_name in city_codes:
        return city_codes[city_name]
    
    # 如果找不到，尝试查找包含该城市名的条目
    for name, code in city_codes.items():
        if city_name in name or name in city_name:
            return code
    
    # 如果输入包含省份信息，尝试解析
    for prov_name in province_codes:
        if city_name.startswith(prov_name):
            # 提取城市名部分
            city_part = city_name[len(prov_name):]
            if city_part:  # 如果还有剩余部分
                # 查找以该省份代码开头且包含城市名部分的城市
                prov_code_prefix = province_codes[prov_name]['code']
                for name, code in city_codes.items():
                    if code.startswith(prov_code_prefix) and city_part in name:
                        return code
    
    return None

def get_province_from_city_code(city_code: str, province_codes: dict):
    """从城市代码推断省份代码"""
    if len(city_code) >= 5:
        prov_code_prefix = city_code[:5]
        for prov_name, prov_info in province_codes.items():
            if prov_info['code'] == prov_code_prefix:
                return prov_name
    return None

def find_cities_by_province(province_name: str, city_codes: dict, province_codes: dict):
    """查找省份下的所有城市"""
    if province_name not in province_codes:
        return []
    
    prov_code = province_codes[province_name]['code']
    province_cities = []
    
    for city_name, city_code in city_codes.items():
        if city_code.startswith(prov_code):
            province_cities.append((city_name, city_code))
    
    return province_cities

def query_weather_com_cn_api_v2(city_code: str) -> Optional[str]:
    """
    使用中国天气网API v2版本
    """
    try:
        # 尝试使用新的API端点
        url = f"http://d1.weather.com.cn/weather_index/{city_code}.shtml"
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            # 尝试解析返回的JSON数据
            try:
                # 查找JSON数据部分
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_part = content[start:end]
                    # 尝试解析为JSON
                    data = json.loads(json_part)
                    
                    # 根据可能的字段名提取数据
                    city = data.get('city', '未知城市')
                    temp = data.get('temp', data.get('real', {}).get('temp', '未知'))
                    weather = data.get('weather', data.get('real', {}).get('weather', '未知'))
                    
                    return f"{city}: {weather} {temp}°C"
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试正则表达式解析
                temp_match = re.search(r'"temp":"([^"]*)"', content)
                weather_match = re.search(r'"weather":"([^"]*)"', content)
                city_match = re.search(r'"city":"([^"]*)"', content)
                
                if temp_match:
                    temp = temp_match.group(1)
                    weather = weather_match.group(1) if weather_match else "天气"
                    city = city_match.group(1) if city_match else "城市"
                    return f"{city}: {weather} {temp}°C"
        
        return None
    except Exception as e:
        print(f"API v2查询失败: {e}", file=sys.stderr)
        return None

def query_weather_com_cn_api_v1(city_code: str) -> Optional[str]:
    """
    使用中国天气网API v1版本（备用）
    """
    try:
        # 尝试使用旧的API端点
        url = f"http://www.weather.com.cn/data/sk/{city_code}.html"
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                real_data = data.get('data', {}).get('real', {})
                
                if real_data:
                    city = real_data.get('city', '未知城市')
                    temp = real_data.get('temp', '未知')
                    weather = real_data.get('weather', '未知')
                    
                    return f"{city}: {weather} {temp}°C"
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试正则表达式
                content = response.text
                temp_match = re.search(r'"temp":"([^"]*)"', content)
                weather_match = re.search(r'"weather":"([^"]*)"', content)
                city_match = re.search(r'"city":"([^"]*)"', content)
                
                if temp_match:
                    temp = temp_match.group(1)
                    weather = weather_match.group(1) if weather_match else "天气"
                    city = city_match.group(1) if city_match else "城市"
                    return f"{city}: {weather} {temp}°C"
        
        return None
    except Exception as e:
        print(f"API v1查询失败: {e}", file=sys.stderr)
        return None

def query_weather_com_cn(city_name: str) -> Optional[str]:
    """
    查询中国天气网API，支持城市代码和省份代码
    """
    # 加载城市和省份代码
    city_codes = load_city_codes()
    province_codes = load_province_codes()
    
    # 查找城市代码
    city_code = find_city_code(city_name, city_codes, province_codes)
    
    if not city_code:
        return None
    
    print(f"使用城市代码: {city_code} 查询 {city_name}")
    
    # 首先尝试API v2
    result = query_weather_com_cn_api_v2(city_code)
    if result:
        print("使用中国天气网API v2")
        return result
    
    # 如果v2失败，尝试API v1
    result = query_weather_com_cn_api_v1(city_code)
    if result:
        print("使用中国天气网API v1")
        return result
    
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

def query_openmeteo_by_city(city_name: str) -> Optional[str]:
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

def is_china_location(location):
    """
    判断位置是否在中国境内
    """
    # 加载城市代码
    city_codes = load_city_codes()
    
    # 使用所有城市名称作为关键词
    china_keywords = list(city_codes.keys())
    
    # 检查是否包含中国关键词
    location_lower = location.lower()
    for keyword in china_keywords:
        if keyword.lower() in location_lower:
            return True
    
    # 检查是否以中国开头或结尾
    if '中国' in location or 'China' in location_lower:
        return True
    
    # 检查省份关键词
    provinces = [
        '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', 
        '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', 
        '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', 
        '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '香港', '澳门'
    ]
    
    for prov in provinces:
        if prov in location:
            return True
    
    return False

def query_fallback_weather(location: str) -> str:
    """
    智能回退天气查询
    当无法查询到具体城市时，自动回退到省级或附近城市
    """
    city_codes = load_city_codes()
    province_codes = load_province_codes()
    
    # 首先尝试直接查询
    direct_result = query_weather_com_cn(location)
    if direct_result:
        return direct_result
    
    # 如果直接查询失败，尝试wttr.in
    wttr_result = query_wttr_in(location)
    if wttr_result:
        return wttr_result
    
    # 如果城市名查询失败，尝试提取省份信息并查询省会
    for prov_name in province_codes:
        if location.startswith(prov_name):
            # 如果是省份+城市的形式，尝试查询省会
            capital_mapping = {
                '北京': '北京', '上海': '上海', '天津': '天津', '重庆': '重庆',
                '河北': '石家庄', '山西': '太原', '内蒙古': '呼和浩特',
                '辽宁': '沈阳', '吉林': '长春', '黑龙江': '哈尔滨',
                '江苏': '南京', '浙江': '杭州', '安徽': '合肥', '福建': '福州', '江西': '南昌', '山东': '济南',
                '河南': '郑州', '湖北': '武汉', '湖南': '长沙',
                '广东': '广州', '广西': '南宁', '海南': '海口',
                '四川': '成都', '贵州': '贵阳', '云南': '昆明',
                '西藏': '拉萨', '陕西': '西安', '甘肃': '兰州', '青海': '西宁', '宁夏': '银川', '新疆': '乌鲁木齐'
            }
            
            if prov_name in capital_mapping:
                capital = capital_mapping[prov_name]
                print(f"未找到 {location} 的具体天气，回退到查询 {prov_name} 省会 {capital}")
                result = query_weather_com_cn(capital)
                if result:
                    return f"[{location} 天气暂无，显示{prov_name}省会] {result}"
                
                # 如果省会也查不到，尝试wttr.in
                result = query_wttr_in(capital)
                if result:
                    return f"[{location} 天气暂无，显示{prov_name}省会] {capital}: {result}"
    
    # 如果是具体城市名但没查到，尝试查找相近的城市
    for city_name in city_codes:
        if location in city_name or city_name in location:
            print(f"未找到 {location} 的具体天气，回退到查询相近城市 {city_name}")
            result = query_weather_com_cn(city_name)
            if result:
                return f"[{location} 天气暂无，显示相近城市] {result}"
    
    # 如果以上都失败，尝试Open-Meteo
    openmeteo_result = query_openmeteo_by_city(location)
    if openmeteo_result:
        return openmeteo_result
    
    # 最后的回退：尝试查询省份
    for prov_name in province_codes:
        if prov_name in location:
            capital_mapping = {
                '北京': '北京', '上海': '上海', '天津': '天津', '重庆': '重庆',
                '河北': '石家庄', '山西': '太原', '内蒙古': '呼和浩特',
                '辽宁': '沈阳', '吉林': '长春', '黑龙江': '哈尔滨',
                '江苏': '南京', '浙江': '杭州', '安徽': '合肥', '福建': '福州', '江西': '南昌', '山东': '济南',
                '河南': '郑州', '湖北': '武汉', '湖南': '长沙',
                '广东': '广州', '广西': '南宁', '海南': '海口',
                '四川': '成都', '贵州': '贵阳', '云南': '昆明',
                '西藏': '拉萨', '陕西': '西安', '甘肃': '兰州', '青海': '西宁', '宁夏': '银川', '新疆': '乌鲁木齐'
            }
            
            if prov_name in capital_mapping:
                capital = capital_mapping[prov_name]
                print(f"未找到 {location} 的具体天气，回退到查询 {prov_name} 省份天气")
                result = query_wttr_in(capital)
                if result:
                    return f"[{location} 天气暂无，显示{prov_name}] {capital}: {result}"
    
    return f"无法获取 {location} 的天气信息，建议尝试查询省会城市或邻近城市"

def query_china_weather(location: str) -> str:
    """
    综合查询中国天气（带智能回退）
    """
    print(f"正在查询: {location}")
    
    if is_china_location(location):
        print("检测到中国境内位置，使用中国天气服务...")
        return query_fallback_weather(location)
    else:
        print("检测到境外位置，使用国际天气服务...")
        # 尝试wttr.in
        result = query_wttr_in(location)
        if result:
            print("使用wttr.in服务")
            return result
        
        # 如果wttr.in失败，尝试Open-Meteo
        result = query_openmeteo_by_city(location)
        if result:
            print("使用Open-Meteo服务")
            return result
        
        return f"无法获取 {location} 的天气信息"

def main():
    if len(sys.argv) < 2:
        print("使用方法: python fallback_enhanced_china_weather.py <城市名称>")
        print("示例: python fallback_enhanced_china_weather.py 北京")
        print("示例: python fallback_enhanced_china_weather.py 上海")
        print("示例: python fallback_enhanced_china_weather.py 浙江嘉兴")
        print("示例: python fallback_enhanced_china_weather.py 某个不存在的城市")
        return
    
    location = sys.argv[1]
    result = query_china_weather(location)
    print(result)

if __name__ == "__main__":
    main()