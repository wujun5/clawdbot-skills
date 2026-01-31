---
name: china-weather
description: Get current weather for China locations using domestic-friendly services. Provides weather information for Chinese cities with fallback to international services when needed. Supports multiple Chinese weather APIs including QWeather and AMap.
metadata: {"clawdbot":{"emoji":"🌧️","requires":{"bins":["curl", "python3", "jq"]}}}
---

# China Weather

Weather information for China using services that work well within China's network environment.

## Quick Start

Simple weather lookup for Chinese cities:
```bash
# Query weather for a Chinese city
bash scripts/china_weather_simple.sh 北京
bash scripts/china_weather_simple.sh 上海
bash scripts/china_weather_simple.sh 杭州
```

## Service Options

### 1. wttr.in (Primary - works for many Chinese cities)

Direct query for Chinese locations:
```bash
curl -s "wttr.in/北京?format=3"
curl -s "wttr.in/上海?format=3"
```

### 2. Chinese Weather Services (Recommended)

For optimal performance in China, configure API keys:

#### QWeather (和风天气)
```bash
export QWEATHER_API_KEY="your_api_key"
bash scripts/china_weather_simple.sh "城市名称"
```

#### AMap Weather (高德地图)
```bash
export AMAP_API_KEY="your_api_key"
bash scripts/china_weather_simple.sh "城市名称"
```

### 3. Open-Meteo with coordinates (Fallback)

For locations not recognized by other services:
```bash
python3 scripts/simple_china_weather.py "城市名称"
```

## Format Options

Use wttr.in format codes:
- `format=3` - Simple format
- `format=1` - More detailed
- Custom formats work with Chinese locations

## API Configuration

### Optional: Configure Chinese Weather APIs

For more accurate results in China, register for API keys:

1. **QWeather**: Visit https://dev.qweather.com
2. **AMap**: Visit https://lbs.amap.com

Set environment variables:
```bash
export QWEATHER_API_KEY="your_qweather_key"
export AMAP_API_KEY="your_amap_key"
```

## Usage Tips

- Major Chinese cities are well-supported by wttr.in
- For more accurate Chinese weather data, use QWeather or AMap API keys
- For less common locations, the system automatically falls back to Open-Meteo
- All outputs are presented in a consistent format
- Chinese weather terms are displayed when available
- The system intelligently selects the best available service based on location