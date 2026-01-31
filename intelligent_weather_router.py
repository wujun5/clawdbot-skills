#!/usr/bin/env python3
"""
智能天气查询路由脚本
根据查询位置自动选择合适的天气服务
"""

import os
import sys
import json
from pathlib import Path

# 添加技能路径
sys.path.append('/home/Tim/BotRoom/clawdbot-skills/china-weather/scripts')

# 导入中国天气模块
from query_china_weather import ChinaWeather

def is_china_location(location):
    """
    判断位置是否在中国境内
    这里使用简单的启发式方法，实际应用中可能需要更精确的地理判断
    """
    # 常见的中国城市/省份关键词
    china_keywords = [
        '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都', '重庆', 
        '天津', '西安', '青岛', '大连', '宁波', '厦门', '苏州', '长沙', '郑州',
        '济南', '福州', '乌鲁木齐', '拉萨', '西宁', '银川', '石家庄', '合肥',
        '太原', '昆明', '南宁', '哈尔滨', '沈阳', '长春', '呼和浩特', '海口',
        '兰州', '银川', '台北', '香港', '澳门', '中国', '中华人民共和国',
        'Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Nanjing',
        'Wuhan', 'Chengdu', 'Chongqing', 'Tianjin', 'Xi\'an', 'Qingdao', 'Dalian',
        'Ningbo', 'Xiamen', 'Suzhou', 'Changsha', 'Zhengzhou', 'Jinan', 'Fuzhou',
        'Urumqi', 'Lhasa', 'Xining', 'Yinchuan', 'Shijiazhuang', 'Hefei', 'Taiyuan',
        'Kunming', 'Nanning', 'Harbin', 'Shenyang', 'Changchun', 'Hohhot', 'Haikou',
        'Lanzhou', 'Taipei', 'Hong Kong', 'Macao'
    ]
    
    # 检查是否包含中国关键词
    location_lower = location.lower()
    for keyword in china_keywords:
        if keyword.lower() in location_lower:
            return True
    
    # 检查是否以中国开头或结尾
    if '中国' in location or 'China' in location_lower:
        return True
    
    return False

def query_weather_intelligent(location):
    """
    智能天气查询 - 根据位置自动选择服务
    """
    print(f"正在分析位置: {location}")
    
    if is_china_location(location):
        print("检测到中国境内位置，使用中国天气服务...")
        # 使用中国天气技能
        weather = ChinaWeather()
        result = weather.query_weather(location)
    else:
        print("检测到境外位置，使用国际天气服务...")
        # 使用原始天气技能 (通过shell命令调用)
        import subprocess
        try:
            cmd = f'curl -s "wttr.in/{location}?format=3"'
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
                
                result = output
            else:
                result = f"无法获取 {location} 的天气信息"
        except Exception as e:
            result = f"国际天气服务查询失败: {str(e)}"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("用法: python intelligent_weather_router.py <城市/国家名称>")
        print("示例: python intelligent_weather_router.py 北京")
        print("示例: python intelligent_weather_router.py London")
        return
    
    location = " ".join(sys.argv[1:])
    result = query_weather_intelligent(location)
    print(result)

if __name__ == "__main__":
    main()