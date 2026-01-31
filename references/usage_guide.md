# 中国天气技能使用指南

## 概述
中国天气技能为国内用户提供可靠的天气信息服务，优先使用国内可访问的天气API，确保在中国网络环境下稳定运行。

## 安装和配置

### 1. 获取API密钥（可选，但推荐）

#### 和风天气API密钥
1. 访问 https://dev.qweather.com/
2. 注册账户
3. 创建应用并获取API密钥
4. 设置环境变量：
   ```bash
   export QWEATHER_API_KEY="你的和风天气API密钥"
   ```

#### 高德地图API密钥
1. 访问 https://lbs.amap.com/
2. 注册开发者账户
3. 创建应用并获取API密钥
4. 设置环境变量：
   ```bash
   export AMAP_API_KEY="你的高德地图API密钥"
   ```

### 2. 环境依赖
- Python 3.x
- requests 库 (可通过 `pip install requests` 安装)

## 使用方法

### Python 模块使用
```python
from scripts.query_china_weather import ChinaWeather

weather = ChinaWeather()
result = weather.query_weather("北京市")
print(result)
```

### 命令行使用
```bash
# 查询天气
python scripts/query_china_weather.py "北京市"
bash scripts/weather_cli.sh "上海市"
```

## 服务优先级
1. 和风天气 (QWeather) - 需要API密钥
2. 高德地图天气 - 需要API密钥
3. Open-Meteo - 国际服务，通常可访问
4. wttr.in - 最后尝试

## 错误处理
- 如果首选服务不可用，自动尝试下一个服务
- 所有API调用都包含异常处理
- 提供清晰的错误信息

## 功能特性
- 中文天气描述
- 多服务冗余保障
- 自动地理编码
- 风向风力信息
- 支持全国城市查询