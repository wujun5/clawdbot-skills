# 中国天气技能 - API集成指南

## 概述

本文档详细介绍了中国天气技能中集成的各种天气API服务，包括使用方式、参数说明和最佳实践。

## 支持的API服务

### 1. wttr.in (国际服务，优先使用)

#### 基本用法
```bash
curl -s "wttr.in/[位置]?format=3"
```

#### 格式参数
- `format=3`: 简洁格式 (推荐)
- `format=1`: 详细格式
- `format=C%20+${t}`: 自定义格式

#### 示例
```bash
curl -s "wttr.in/北京?format=3"
curl -s "wttr.in/上海?format=3"
curl -s "wttr.in/杭州西湖?format=3"
```

### 2. Open-Meteo (国际服务，备用)

#### 基本用法
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=[纬度]&longitude=[经度]&current_weather=true"
```

#### 参数说明
- `latitude`: 纬度坐标
- `longitude`: 经度坐标
- `current_weather=true`: 获取当前天气
- `temperature_unit=celsius`: 摄氏度单位
- `windspeed_unit=kmh`: 风速单位为公里/小时

### 3. 中国天气网 (国内服务)

#### 基本用法
```bash
curl -s "http://www.weather.com.cn/data/sk/[城市代码].html"
```

#### 城市代码对照表 (常用)
- 北京: 101010100
- 上海: 101020100
- 广州: 101280101
- 深圳: 101280601
- 杭州: 101210101
- 南京: 101190101
- 武汉: 101200101
- 成都: 101270101
- 重庆: 101040100
- 西安: 101110101

### 4. 和风天气 (国内服务，需API密钥)

#### 注册和获取API密钥
1. 访问 https://dev.qweather.com
2. 注册账户
3. 创建应用获取API密钥

#### 当前天气查询
```bash
curl -s "https://devapi.qweather.com/v7/weather/now?location=[城市ID]&key=[API_KEY]"
```

#### 城市搜索
```bash
curl -s "https://geoapi.qweather.com/v2/city/lookup?location=[城市名]&key=[API_KEY]"
```

### 5. 高德地图天气 (国内服务，需API密钥)

#### 注册和获取API密钥
1. 访问 https://lbs.amap.com
2. 注册开发者账户
3. 创建应用获取API密钥

#### 基础天气查询
```bash
curl -s "https://restapi.amap.com/v3/weather/weatherInfo?key=[API_KEY]&city=[城市编码]&extensions=base"
```

#### 获取城市编码
```bash
curl -s "https://restapi.amap.com/v3/config/district?keywords=[城市名]&subdistrict=0&key=[API_KEY]"
```

## 服务优先级和选择逻辑

### 中国境内位置查询逻辑
1. **有和风天气API密钥**: 使用和风天气API
2. **有高德地图API密钥**: 使用高德地图天气API
3. **无API密钥**: 尝试wttr.in
4. **wttr.in失败**: 使用Open-Meteo（通过坐标查询）

### 国际位置查询逻辑
1. **直接使用wttr.in**
2. **wttr.in失败**: 使用Open-Meteo

## 实际使用示例

### Bash脚本集成示例
```bash
#!/bin/bash

# 环境变量检查
QWEATHER_KEY="${QWEATHER_API_KEY:-}"
AMAP_KEY="${AMAP_API_KEY:-}"

query_china_weather() {
    local location="$1"
    
    # 如果有和风天气密钥，优先使用
    if [ -n "$QWEATHER_KEY" ]; then
        # 获取城市ID
        city_id=$(curl -s "https://geoapi.qweather.com/v2/city/lookup?location=${location}&key=${QWEATHER_KEY}" | jq -r '.location[0].id')
        if [ -n "$city_id" ] && [ "$city_id" != "null" ]; then
            weather_data=$(curl -s "https://devapi.qweather.com/v7/weather/now?location=${city_id}&key=${QWEATHER_KEY}")
            temp=$(echo $weather_data | jq -r '.now.temp')
            text=$(echo $weather_data | jq -r '.now.text')
            echo "${location}: ${text} ${temp}°C"
            return 0
        fi
    fi
    
    # 如果有高德密钥，使用高德
    if [ -n "$AMAP_KEY" ]; then
        city_code=$(curl -s "https://restapi.amap.com/v3/config/district?keywords=${location}&subdistrict=0&key=${AMAP_KEY}" | jq -r '.districts[0].citycode')
        if [ -n "$city_code" ] && [ "$city_code" != "null" ]; then
            weather_data=$(curl -s "https://restapi.amap.com/v3/weather/weatherInfo?key=${AMAP_KEY}&city=${city_code}&extensions=base")
            weather_text=$(echo $weather_data | jq -r '.lives[0].weather')
            temperature=$(echo $weather_data | jq -r '.lives[0].temperature')
            echo "${location}: ${weather_text} ${temperature}°C"
            return 0
        fi
    fi
    
    # 回退到wttr.in
    result=$(curl -s "wttr.in/${location}?format=3")
    if [ -n "$result" ] && [ "$result" != "Unknown location" ]; then
        echo "$result"
        return 0
    fi
    
    # 最后尝试Open-Meteo
    # (需要先获取坐标，这里省略详细实现)
    
    echo "无法获取 ${location} 的天气信息"
    return 1
}
```

## 配置建议

### 环境变量设置
```bash
# 可选：设置API密钥以获得更准确的数据
export QWEATHER_API_KEY="your_qweather_api_key"
export AMAP_API_KEY="your_amap_api_key"
```

### 使用示例
```bash
# 设置环境变量后
bash scripts/china_weather_simple.sh "北京市"
bash scripts/china_weather_simple.sh "杭州市西湖区"
```

## 注意事项

1. **API配额限制**: 大多数API服务都有调用次数限制
2. **网络连通性**: 不同服务在中国网络环境下的访问速度可能不同
3. **数据更新频率**: 不同服务的数据更新频率不同
4. **中文支持**: 国内服务通常提供更好的中文支持

通过合理配置和使用这些API服务，可以获得最稳定和准确的中国天气信息。