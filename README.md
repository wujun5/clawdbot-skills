# Clawdbot Skills Repository

This repository contains custom skills for Clawdbot, an AI assistant framework. Each skill extends Clawdbot's capabilities in specific domains.

## Skills Included

### China Weather Skill (`china-weather`)

A weather skill specifically designed for use in China, utilizing domestic weather services that are reliably accessible within China's network environment.

#### Features:
- Prioritizes Chinese weather services (QWeather, AMap)
- Fallback to international services when needed
- Full Chinese localization
- Multi-service redundancy for high availability
- Easy integration with Clawdbot

#### Services Supported:
1. **QWeather (和风天气)** - Primary service (API key required)
2. **AMap Weather (高德地图)** - Secondary service (API key required)  
3. **Open-Meteo** - Fallback international service
4. **wttr.in** - Last resort service

#### Installation:
1. Clone this repository
2. Install the skill in your Clawdbot instance
3. (Optional) Set environment variables for premium services:
   ```bash
   export QWEATHER_API_KEY="your_key_here"
   export AMAP_API_KEY="your_key_here"
   ```

#### Usage:
```python
from scripts.query_china_weather import ChinaWeather

weather = ChinaWeather()
result = weather.query_weather("北京市")
print(result)  # Output: 北京: 晴 22°C 风速:10km/h
```

## Repository Structure

```
clawdbot-skills/
├── china-weather/          # China Weather skill
│   ├── SKILL.md           # Skill definition and documentation
│   ├── scripts/            # Executable scripts
│   │   ├── query_china_weather.py
│   │   └── weather_cli.sh
│   └── references/         # Reference documents
│       └── usage_guide.md
├── china_weather_skill_creation_process.md  # Development documentation
└── README.md              # This file
```

## Contributing

Feel free to contribute additional skills that enhance Clawdbot's functionality. Each skill should follow the standard structure:

- `SKILL.md` - Skill definition with YAML frontmatter
- `scripts/` - Executable code
- `references/` - Reference documentation
- `assets/` - Static assets (if needed)

## License

See individual skill directories for license information.