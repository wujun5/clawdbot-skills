#!/bin/bash
# China Weather - Simplified version mimicking original weather skill

query_china_weather() {
    local location="$1"
    
    if [ -z "$location" ]; then
        echo "Usage: $0 <location>"
        echo "Examples:"
        echo "  $0 北京"
        echo "  $0 上海"
        echo "  $0 杭州西湖"
        return 1
    fi
    
    # Method 1: Try wttr.in directly (works for many Chinese cities)
    result=$(curl -s "wttr.in/$location?format=3" 2>/dev/null)
    
    if [ -n "$result" ] && ! echo "$result" | grep -q "Unknown location\|ERROR"; then
        # Translate basic English weather terms to Chinese
        output=$(echo "$result" | sed \
            -e 's/Cloudy/多云/g' \
            -e 's/Overcast/阴/g' \
            -e 's/Clear/晴/g' \
            -e 's/Sunny/晴/g' \
            -e 's/Partly cloudy/晴间多云/g' \
            -e 's/Rain/雨/g' \
            -e 's/Shower/阵雨/g' \
            -e 's/Snow/雪/g' \
            -e 's/Fog/雾/g' \
            -e 's/Thunderstorm/雷暴/g' \
            -e 's/Moderate rain/中雨/g' \
            -e 's/Heavy rain/大雨/g' \
            -e 's/Light rain/小雨/g')
        
        echo "$output"
        return 0
    fi
    
    # Method 2: Use Python script to resolve coordinates and query Open-Meteo
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PYTHON_SCRIPT="$SCRIPT_DIR/simple_china_weather.py"
    
    if command -v python3 >/dev/null 2>&1 && [ -f "$PYTHON_SCRIPT" ]; then
        python3 "$PYTHON_SCRIPT" "$location"
        return $?
    fi
    
    # If all methods fail
    echo "Cannot retrieve weather for: $location"
    return 1
}

# Execute the function with the given argument
query_china_weather "$1"