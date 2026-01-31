---
name: china-weather
description: Comprehensive weather information retrieval for China using domestic services like QWeather and AMap. Provides current weather, forecasts, and air quality data for Chinese cities without relying on blocked international services. Use when users need weather information for locations in China, especially when international weather services are inaccessible.
---

# China Weather

## Overview

China Weather skill provides comprehensive weather information for Chinese locations using domestic APIs that are accessible within China's network environment. It integrates multiple Chinese weather services including QWeather (和风天气) and AMap (高德地图) to ensure reliable weather data access.

## Usage Scenarios

Use this skill when:
- Providing weather information for Chinese cities
- International weather services are blocked or slow to access
- Need accurate weather data for locations in China
- Users specifically request weather information within China
- Air quality information is needed for Chinese cities

## Quick Start

Basic weather query:
```bash
# Query weather for a Chinese city
query_weather_cn "北京"
query_weather_cn "上海"
query_weather_cn "广州"
```

## Service Priority and Fallback

The skill implements a service priority system to ensure maximum availability:

1. **QWeather (和风天气)** - Primary service (requires API key)
2. **AMap (高德地图)** - Secondary service (requires API key)  
3. **Open-Meteo** - Fallback international service (often accessible)
4. **wttr.in** - Last resort service

## Configuration

### API Keys (Optional but Recommended)

To use premium Chinese weather services:

- **QWeather API Key**: Register at https://dev.qweather.com/
- **AMap API Key**: Register at https://lbs.amap.com/

Set environment variables:
```bash
export QWEATHER_API_KEY="your_key_here"
export AMAP_API_KEY="your_key_here"
```

### Scripts Included

The skill includes several utility scripts in the `scripts/` directory:

- `query_china_weather.py` - Main Python weather querying script
- `weather_cli.sh` - Command-line interface for weather queries
- `coordinates_resolver.py` - Geographic coordinate resolver using domestic services

## Core Functions

### 1. Current Weather Query

```python
# Python usage
from china_weather import query_weather
result = query_weather("北京市")
print(result)  # Output: 北京: 晴 22°C 风速:10km/h
```

### 2. Forecast Query

```python
# Get 3-day forecast
result = query_forecast("上海市", days=3)
```

### 3. Air Quality Query

```python
# Get air quality information
aqi_data = query_air_quality("广州市")
```

## Error Handling

The skill implements graceful fallback mechanisms:
- If primary service fails, automatically tries secondary service
- If all domestic services fail, attempts international services
- If no services are available, returns appropriate error message

## Features

- **Chinese localization**: All weather descriptions in Chinese
- **Multiple service redundancy**: Ensures high availability
- **Geographic resolution**: Automatic location-to-coordinates conversion
- **Air quality data**: Includes AQI and pollutant information
- **Forecast support**: Multi-day forecasts available
- **Precipitation data**: Rain/snow probability and accumulation
- **Wind information**: Direction, speed, and gust data

## Performance Optimization

- **Local caching**: Frequently accessed locations cached locally
- **Coordinate pre-resolution**: Common locations resolved in advance
- **Service health monitoring**: Automatically avoids failing services
- **Efficient data transfer**: Minimal payload for faster responses

## Integration with Clawdbot

The skill integrates seamlessly with Clawdbot's tool system and can be called programmatically when weather information for Chinese locations is requested.