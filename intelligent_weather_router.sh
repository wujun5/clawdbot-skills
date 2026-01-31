#!/bin/bash
# 智能天气查询路由脚本
# 根据位置自动选择合适的天气服务

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -eq 0 ]; then
    echo "用法: $0 <城市/国家名称>"
    echo "示例: $0 北京"
    echo "示例: $0 London"
    exit 1
fi

LOCATION="$*"

# 使用Python路由脚本
python3 "${SCRIPT_DIR}/intelligent_weather_router.py" "$LOCATION"