#!/bin/bash
# 中国天气查询命令行工具

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

query_china_weather() {
    local location="$1"
    
    if [ -z "$location" ]; then
        echo "用法: $0 <城市名称>"
        echo "示例: $0 北京"
        echo "示例: $0 上海"
        return 1
    fi
    
    # 尝试执行Python脚本
    if command -v python3 >/dev/null 2>&1; then
        python3 "${SCRIPT_DIR}/query_china_weather.py" "$location"
    else
        echo "错误: 未找到python3命令"
        return 1
    fi
}

# 主程序
query_china_weather "$1"