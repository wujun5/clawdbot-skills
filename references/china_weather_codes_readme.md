# 中国天气网城市代码获取与使用说明

## 概述

本项目包含了从中国天气网（weather.com.cn）获取的中国各城市天气代码，用于快速查询中国境内城市的天气信息。

## 城市代码文件

### complete_china_weather_city_codes.json
- 包含375个中国主要城市和地区的天气代码
- 代码格式：101XXYYYYZ
  - 101: 固定前缀
  - XX: 省份代码
  - YYYY: 城市代码
  - Z: 区域代码

### 城市分布统计
- 北京: 3 个城市
- 上海: 3 个城市
- 广东: 30 个城市
- 四川: 21 个城市
- 湖北: 17 个城市
- 山东: 17 个城市
- 江苏: 13 个城市
- 浙江: 12 个城市
以及其他省份和自治区的城市

## API使用方法

### 中国天气网实时天气API
```
GET http://d1.weather.com.cn/sk_2d/{城市代码}.html
```

示例：
- 北京: `http://d1.weather.com.cn/sk_2d/101010100.html`
- 上海: `http://d1.weather.com.cn/sk_2d/101020100.html`
- 广州: `http://d1.weather.com.cn/sk_2d/101280101.html`

### 响应数据格式
API返回JavaScript格式的数据，包含以下字段：
- `city`: 城市名称
- `temp`: 当前温度
- `WD`: 风向
- `WS`: 风力
- `SD`: 湿度
- `time`: 更新时间

## 使用示例

### Python使用示例
```python
import requests
import json
import re

# 加载城市代码
with open('complete_china_weather_city_codes.json', 'r', encoding='utf-8') as f:
    city_codes = json.load(f)

# 查询北京天气
city_code = city_codes.get('北京')
if city_code:
    url = f'http://d1.weather.com.cn/sk_2d/{city_code}.html'
    headers = {
        'Referer': 'http://www.weather.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.text
        # 解析天气信息
        import re
        city_match = re.search(r'"city":"([^"]*)"', content)
        temp_match = re.search(r'"temp":"([^"]*)"', content)
        weather_match = re.search(r'"weather":"([^"]*)"', content)
        
        if city_match and temp_match:
            city_name = city_match.group(1)
            temp = temp_match.group(1)
            weather = weather_match.group(1) if weather_match else '未知'
            print(f'{city_name}: {weather} {temp}°C')
```

### Bash使用示例
```bash
# 使用curl查询天气
CITY_CODE="101010100"  # 北京
curl -H "Referer: http://www.weather.com.cn/" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "http://d1.weather.com.cn/sk_2d/${CITY_CODE}.html"
```

## 注意事项

1. **请求频率限制**: 请勿过于频繁地请求API，以免被封IP
2. **User-Agent**: 必须设置适当的User-Agent头部
3. **Referer**: 需要设置Referer头部
4. **数据格式**: 响应为JavaScript格式，需要适当解析
5. **编码**: 响应可能使用GBK或UTF-8编码

## 城市代码更新

城市代码相对稳定，一般不会频繁变动。如需更新，可以：
1. 使用提供的`get_complete_china_weather_codes.py`脚本重新获取
2. 手动添加新的城市代码

## 法律声明

本项目仅用于学习和研究目的，请遵守中国天气网的相关使用规定，不得用于商业用途或大规模数据采集。