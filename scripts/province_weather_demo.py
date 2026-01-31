#!/usr/bin/env python3
"""
使用省份代码获取省级天气概览
"""

import json
import requests
import re
from typing import Dict, List

def load_province_codes():
    """加载省份代码"""
    try:
        with open('scripts/china_weather_province_codes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，返回空字典
        return {}

def get_city_codes_by_province(province_code: str) -> List[tuple]:
    """根据省份代码获取该省主要城市的代码"""
    # 这里我们可以从完整的城市代码列表中筛选
    try:
        with open('scripts/complete_china_weather_city_codes.json', 'r', encoding='utf-8') as f:
            all_cities = json.load(f)
    except FileNotFoundError:
        return []
    
    province_cities = []
    for city_name, city_code in all_cities.items():
        if city_code.startswith(province_code):
            province_cities.append((city_name, city_code))
    
    return province_cities

def get_province_weather_overview(province_name: str) -> str:
    """获取省份天气概览"""
    province_codes = load_province_codes()
    
    if province_name not in province_codes:
        return f"未找到省份: {province_name}"
    
    province_code = province_codes[province_name]["code"]
    
    # 获取该省的主要城市
    cities = get_city_codes_by_province(province_code)
    
    if not cities:
        return f"未找到 {province_name} 的城市数据"
    
    # 获取第一个城市的天气作为省份概览
    first_city_name, first_city_code = cities[0]
    
    try:
        url = f"http://d1.weather.com.cn/sk_2d/{first_city_code}.html"
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # 解析天气信息
            temp_match = re.search(r'"temp":"([^"]*)"', content)
            weather_match = re.search(r'"weather1":"([^"]*)"', content)
            if not weather_match:
                weather_match = re.search(r'"weather":"([^"]*)"', content)
            
            if temp_match:
                temp = temp_match.group(1)
                weather = weather_match.group(1) if weather_match else "未知"
                
                return f"{province_name}({first_city_name}): {weather} {temp}°C"
            else:
                return f"{province_name}: 无法解析天气数据"
        else:
            return f"{province_name}: 请求失败 (状态码: {response.status_code})"
    
    except Exception as e:
        return f"{province_name}: 请求异常 - {str(e)}"

def get_all_provinces_weather():
    """获取所有省份的天气概览"""
    province_codes = load_province_codes()
    
    print("中国各省份天气概览:")
    print("=" * 40)
    
    for province_name in province_codes:
        weather_info = get_province_weather_overview(province_name)
        print(weather_info)

def main():
    """主函数"""
    print("使用省份代码获取天气信息...")
    
    # 示例：获取北京天气
    beijing_weather = get_province_weather_overview("北京")
    print(f"北京天气: {beijing_weather}")
    
    # 示例：获取广东省天气
    guangdong_weather = get_province_weather_overview("广东")
    print(f"广东天气: {guangdong_weather}")
    
    print("\n输入省份名称查询天气，例如：")
    print("- 北京")
    print("- 上海") 
    print("- 广东")
    print("- 浙江")
    print("- 四川")

if __name__ == "__main__":
    main()