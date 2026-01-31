# 智能天气查询系统

## 概述

智能天气查询系统是一个高级天气查询解决方案，它能够根据查询位置自动选择最适合的天气服务：

- 当查询中国境内位置时，优先使用国内天气服务（和风天气、高德地图等）
- 当查询境外位置时，使用国际天气服务（wttr.in、Open-Meteo等）

## 功能特点

### 1. 智能位置检测
- 自动识别中国境内城市和地点
- 支持中文和英文地名识别
- 包含中国主要城市、省份和地区的关键词库

### 2. 服务自动路由
- 中国境内 → 中国天气技能（优先级：和风天气 > 高德地图 > Open-Meteo > wttr.in）
- 中国境外 → 国际天气技能（优先级：wttr.in > Open-Meteo）

### 3. 统一接口
- 提供统一的查询接口
- 相同的输出格式
- 透明的服务切换

## 使用方法

### Python 接口
```python
from intelligent_weather_router import query_weather_intelligent

result = query_weather_intelligent("北京市")
print(result)  # 使用中国天气服务

result = query_weather_intelligent("London")
print(result)  # 使用国际天气服务
```

### 命令行接口
```bash
# 查询中国城市
./intelligent_weather_router.sh 北京
./intelligent_weather_router.sh 上海

# 查询国际城市
./intelligent_weather_router.sh London
./intelligent_weather_router.sh New York
```

## 配置选项

### API密钥配置（可选，但推荐）
为了获得最佳的中国天气服务体验，可以配置API密钥：

```bash
export QWEATHER_API_KEY="your_qweather_api_key"
export AMAP_API_KEY="your_amap_api_key"
```

### 位置检测自定义
如果需要更精确的位置检测，可以修改 `is_china_location()` 函数中的关键词库。

## 工作原理

1. 接收位置查询请求
2. 使用关键词匹配算法判断位置是否在中国境内
3. 根据结果选择相应的天气服务
4. 返回格式化的天气信息

## 故障处理

- 如果首选服务不可用，系统会自动尝试下一优先级的服务
- 所有服务都不可用时，返回错误信息
- 网络超时设置为10秒，避免长时间等待

## 优势

- **高可用性**：多服务冗余保证
- **最佳性能**：根据位置选择最快的服务
- **用户体验**：自动适配，无需手动选择
- **兼容性**：保留所有原有功能
- **可扩展性**：易于添加新的服务或位置检测规则

## 技术架构

```
用户查询
    ↓
位置检测
    ↓
服务路由
    ├── 中国境内 → 中国天气技能
    └── 中国境外 → 国际天气技能
    ↓
统一输出格式
```

## 部署建议

建议将此智能路由系统作为主要的天气查询接口，逐步取代单独的天气技能调用，以获得最佳的用户体验。