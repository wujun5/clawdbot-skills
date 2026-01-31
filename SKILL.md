---
name: china-weather
description: Get current weather for China locations using domestic-friendly services. Provides weather information for Chinese cities with fallback to international services when needed.
metadata: {"clawdbot":{"emoji":"🌧️","requires":{"bins":["curl", "python3"]}}}
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

### 2. Open-Meteo with coordinates (Fallback)

For locations not recognized by wttr.in:
```bash
python3 scripts/simple_china_weather.py "城市名称"
```

## Format Options

Use wttr.in format codes:
- `format=3` - Simple format
- `format=1` - More detailed
- Custom formats work with Chinese locations

## Usage Tips

- Major Chinese cities are well-supported by wttr.in
- For less common locations, use the Python script which resolves to coordinates
- The system automatically falls back to Open-Meteo if wttr.in fails
- All outputs are presented in a consistent format
- Chinese weather terms are displayed when available