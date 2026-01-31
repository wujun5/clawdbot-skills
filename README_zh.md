# Clawdbot 技能仓库

这个仓库包含为 Clawdbot 设计的自定义技能，每个技能都扩展了 Clawdbot 在特定领域的能力。

## 包含的技能

### 中国天气技能 (`china-weather`)

专门为在中国境内使用而设计的天气技能，利用国内天气服务，确保在中国网络环境下的稳定访问。

#### 功能特点：
- 优先使用中国天气服务（和风天气、高德地图）
- 需要时回退到国际服务
- 完全中文本地化
- 多服务冗余以确保高可用性
- 与 Clawdbot 无缝集成

#### 支持的服务：
1. **和风天气 (QWeather)** - 主要服务（需要API密钥）
2. **高德地图天气 (AMap Weather)** - 备用服务（需要API密钥）
3. **Open-Meteo** - 备用国际服务
4. **wttr.in** - 最后备选服务

#### 安装方法：
1. 克隆此仓库
2. 在您的 Clawdbot 实例中安装技能
3. （可选）设置环境变量以使用付费服务：
   ```bash
   export QWEATHER_API_KEY="您的和风天气密钥"
   export AMAP_API_KEY="您的高德地图密钥"
   ```

#### 使用方法：
```python
from scripts.query_china_weather import ChinaWeather

weather = ChinaWeather()
result = weather.query_weather("北京市")
print(result)  # 输出: 北京: 晴 22°C 风速:10km/h
```

### 智能天气路由器

一个高级天气查询解决方案，能够根据查询位置自动选择最适合的天气服务：

- **中国位置** → 中国天气技能（和风天气、高德地图等）
- **国际位置** → 国际天气服务（wttr.in、Open-Meteo等）

#### 功能特点：
- 自动位置检测
- 智能服务路由
- 统一接口
- 无论位置如何都能提供无缝体验
- 与现有系统保持兼容

## 仓库结构

```
clawdbot-skills/
├── china-weather/          # 中国天气技能
│   ├── SKILL.md           # 技能定义和文档
│   ├── scripts/            # 可执行脚本
│   │   ├── query_china_weather.py
│   │   └── weather_cli.sh
│   └── references/         # 参考文档
│       └── usage_guide.md
├── china_weather_skill_creation_process.md  # 开发过程文档
├── intelligent_weather_router.py           # 智能路由系统
├── intelligent_weather_router.sh           # 智能路由系统（Shell版）
├── intelligent_weather_system.md           # 智能系统说明文档
├── clawdbot_weather_config.ini             # 配置文件
├── china-weather.skill                     # 打包的技能文件
└── README.md                              # 本文件
```

## 如何贡献

欢迎贡献能够增强 Clawdbot 功能的额外技能。每个技能都应该遵循标准结构：

- `SKILL.md` - 带有YAML前言的技能定义
- `scripts/` - 可执行代码
- `references/` - 参考文档
- `assets/` - 静态资源（如果需要）

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。