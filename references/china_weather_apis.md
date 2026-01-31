# 中国天气服务API使用指南

## 1. 中国天气网 (weather.com.cn)

### 基本信息
- 官网: http://www.weather.com.cn
- 数据源: 中国气象局

### API使用方式
中国天气网提供以下几种数据获取方式:

#### A. 公开数据接口 (无需API密钥)
```bash
# 获取某城市天气 (通过城市代码)
curl "http://www.weather.com.cn/data/sk/[城市代码].html"
curl "http://www.weather.com.cn/data/cityinfo/[城市代码].html"

# 城市代码示例:
# 北京: 101010100
# 上海: 101020100
# 广州: 101280101
# 深圳: 101280601
```

#### B. 省份天气数据
```bash
# 获取省份天气概览
curl "http://d1.weather.com.cn/sk_2d/[省份代码].html"
```

### 城市代码对照表 (常用)
```
北京: 101010100
上海: 101020100
广州: 101280101
深圳: 101280601
杭州: 101210101
南京: 101190101
武汉: 101200101
成都: 101270101
重庆: 101040100
西安: 101110101
```

## 2. 和风天气 (QWeather)

### 基本信息
- 官网: https://dev.qweather.com
- 需要注册获取API密钥

### API使用方式

#### A. 当前天气
```bash
# 使用城市ID查询
curl "https://devapi.qweather.com/v7/weather/now?location=[城市ID]&key=[API_KEY]"

# 使用经纬度查询
curl "https://devapi.qweather.com/v7/weather/now?location=[经度],[纬度]&key=[API_KEY]"
```

#### B. 3天天气预报
```bash
curl "https://devapi.qweather.com/v7/weather/3d?location=[城市ID]&key=[API_KEY]"
```

#### C. 城市搜索
```bash
curl "https://geoapi.qweather.com/v2/city/lookup?location=[城市名]&key=[API_KEY]"
```

### 城市ID获取
- 通过geoapi.qweather.com/v2/city/lookup接口获取
- 或使用经纬度直接查询

## 3. 高德地图天气API

### 基本信息
- 需要高德开放平台账号和API密钥
- 官网: https://lbs.amap.com/api/webservice/guide/api/weatherinfo

### API使用方式

#### A. 基础天气查询
```bash
# 根据城市编码查询天气
curl "https://restapi.amap.com/v3/weather/weatherInfo?key=[API_KEY]&city=[城市编码]&extensions=base"

# 根据城市名称查询天气
curl "https://restapi.amap.com/v3/weather/weatherInfo?key=[API_KEY]&city=[城市名称]&extensions=base"
```

#### B. 详细天气预报
```bash
# 扩展预报
curl "https://restapi.amap.com/v3/weather/weatherInfo?key=[API_KEY]&city=[城市编码]&extensions=all"
```

### 城市编码获取
```bash
# 通过地名获取城市编码
curl "https://restapi.amap.com/v3/config/district?keywords=[城市名]&subdistrict=0&key=[API_KEY]"
```

## 4. 彩云天气

### 基本信息
- 官网: https://caiyunapp.com
- 提供分钟级天气预报

### API使用方式

#### A. 天气查询
```bash
# 彩云天气API (需要注册获取token)
curl "https://api.caiyunapp.com/v2.5/[TOKEN]/[经度],[纬度]/weather.json"
```

## 5. 实际应用示例

### Bash脚本示例
```bash
#!/bin/bash

# 和风天气查询函数
query_qweather() {
    local location=$1
    local api_key=$2
    
    # 首先搜索城市ID
    city_info=$(curl -s "https://geoapi.qweather.com/v2/city/lookup?location=${location}&key=${api_key}")
    city_id=$(echo $city_info | jq -r '.location[0].id')
    
    if [ "$city_id" != "null" ]; then
        # 查询当前天气
        weather=$(curl -s "https://devapi.qweather.com/v7/weather/now?location=${city_id}&key=${api_key}")
        temp=$(echo $weather | jq -r '.now.temp')
        text=$(echo $weather | jq -r '.now.text')
        echo "${location}: ${text} ${temp}°C"
    else
        echo "无法找到位置: ${location}"
    fi
}

# 高德地图天气查询函数
query_amap_weather() {
    local city=$1
    local api_key=$2
    
    # 获取城市编码
    city_info=$(curl -s "https://restapi.amap.com/v3/config/district?keywords=${city}&subdistrict=0&key=${api_key}")
    city_code=$(echo $city_info | jq -r '.districts[0].citycode')
    
    if [ "$city_code" != "null" ]; then
        # 查询天气
        weather=$(curl -s "https://restapi.amap.com/v3/weather/weatherInfo?key=${api_key}&city=${city_code}&extensions=base")
        weather_info=$(echo $weather | jq -r '.lives[0]')
        weather_text=$(echo $weather_info | jq -r '.weather')
        temperature=$(echo $weather_info | jq -r '.temperature')
        echo "${city}: ${weather_text} ${temperature}°C"
    else
        echo "无法找到城市: ${city}"
    fi
}
```

### 注意事项
1. 大多数API都需要注册获取API密钥
2. 有免费配额限制，超出需付费
3. 需要遵守各服务商的使用条款
4. 部分服务需要企业认证才能获取API密钥