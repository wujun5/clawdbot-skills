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
sys.path.append('/home/Tim/BotRoom/skills_workspace/china-weather/scripts')

# 导入带有中国天气网API的模块
from china_weather_with_cnn import query_weather_com_cn, query_wttr_in, query_opentempero_by_city

def is_china_location(location):
    """
    判断位置是否在中国境内
    这里使用简单的启发式方法，实际应用中可能需要更精确的地理判断
    """
    # 从完整城市代码中提取城市名称作为关键词
    import os
    import sys
    import json
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    city_codes_file = os.path.join(script_dir, '..', 'clawdbot-skills', 'scripts', 'complete_china_weather_city_codes.json')
    
    # 尝试从当前目录寻找
    if not os.path.exists(city_codes_file):
        city_codes_file = os.path.join(script_dir, 'complete_china_weather_city_codes.json')
    
    # 再尝试在技能目录中寻找
    if not os.path.exists(city_codes_file):
        city_codes_file = os.path.join('/home/Tim/BotRoom/skills_workspace/china-weather/scripts', 'complete_china_weather_city_codes.json')
    
    # 最后尝试在当前工作目录寻找
    if not os.path.exists(city_codes_file):
        city_codes_file = '/home/Tim/BotRoom/complete_china_weather_city_codes.json'
    
    try:
        with open(city_codes_file, 'r', encoding='utf-8') as f:
            city_codes = json.load(f)
        # 使用所有城市名称作为关键词
        china_keywords = list(city_codes.keys())
    except FileNotFoundError:
        # 如果文件不存在，使用原始的关键词列表
        china_keywords = [
            # 直辖市
            '北京', '上海', '天津', '重庆',
            # 主要城市
            '广州', '深圳', '杭州', '南京', '武汉', '成都', '西安', '青岛', '大连', 
            '宁波', '厦门', '苏州', '长沙', '郑州', '济南', '福州', '南昌',
            # 其他重要城市
            '乌鲁木齐', '拉萨', '西宁', '银川', '石家庄', '合肥', '太原', '昆明', 
            '南宁', '哈尔滨', '沈阳', '长春', '呼和浩特', '海口', '兰州',
            # 特殊行政区
            '台北', '香港', '澳门',
            # 省份
            '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', 
            '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', 
            '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', 
            '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾',
            # 国家名称
            '中国', '中华人民共和国', 'PRC', 'China',
            # 英文城市名
            'Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Nanjing',
            'Wuhan', 'Chengdu', 'Chongqing', 'Tianjin', 'Xi\'an', 'Qingdao', 'Dalian',
            'Ningbo', 'Xiamen', 'Suzhou', 'Changsha', 'Zhengzhou', 'Jinan', 'Fuzhou',
            'Nanchang', 'Urumqi', 'Lhasa', 'Xining', 'Yinchuan', 'Shijiazhuang', 
            'Hefei', 'Taiyuan', 'Kunming', 'Nanning', 'Harbin', 'Shenyang', 'Changchun', 
            'Hohhot', 'Haikou', 'Lanzhou', 'Taipei', 'Hong Kong', 'Macao'
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
        # 使用集成中国天气网API的中国天气技能
        
        # 首先尝试中国天气网API（国内服务，通常最快）
        result = query_weather_com_cn(location)
        if result:
            print("使用中国天气网服务")
            return result
        
        # 如果中国天气网失败，尝试wttr.in
        result = query_wttr_in(location)
        if result:
            print("使用wttr.in服务")
            return result
        
        # 如果wttr.in也失败，尝试Open-Meteo
        result = query_opentempero_by_city(location)
        if result:
            print("使用Open-Meteo服务")
            return result
        
        return f"无法获取 {location} 的天气信息"
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