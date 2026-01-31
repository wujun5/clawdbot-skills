#!/bin/bash
# Simplified China Weather script mimicking the original weather skill

query_china_weather() {
    local location="$1"
    
    if [ -z "$location" ]; then
        echo "Usage: $0 <location>"
        echo "Example: $0 北京"
        echo "Example: $0 上海"
        return 1
    fi
    
    echo "Querying weather for: $location"
    
    # First, try wttr.in with the location
    echo "Trying wttr.in service..."
    result=$(curl -s "wttr.in/$location?format=3" 2>/dev/null)
    
    if [ -n "$result" ] && [ "$result" != "Unknown location" ]; then
        # Translate common English terms to Chinese if needed
        translated_result="$result"
        # Basic translation of common weather terms
        translated_result=$(echo "$translated_result" | sed 's/Cloudy/多云/g')
        translated_result=$(echo "$translated_result" | sed 's/Overcast/阴/g')
        translated_result=$(echo "$translated_result" | sed 's/Clear/晴/g')
        translated_result=$(echo "$translated_result" | sed 's/Sunny/晴/g')
        translated_result=$(echo "$translated_result" | sed 's/Rain/雨/g')
        translated_result=$(echo "$translated_result" | sed 's/Shower/阵雨/g')
        translated_result=$(echo "$translated_result" | sed 's/Snow/雪/g')
        translated_result=$(echo "$translated_result" | sed 's/Fog/雾/g')
        translated_result=$(echo "$translated_result" | sed 's/Thunder/雷/g')
        
        echo "$translated_result"
        return 0
    fi
    
    # If wttr.in fails, try to get coordinates and use Open-Meteo
    echo "wttr.in failed, trying alternative method..."
    
    # Attempt to use Python script for location resolution
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PYTHON_SCRIPT="$SCRIPT_DIR/../scripts/enhanced_query_china_weather.py"
    
    if command -v python3 >/dev/null 2>&1 && [ -f "$PYTHON_SCRIPT" ]; then
        python3 "$PYTHON_SCRIPT" "$location"
        return $?
    fi
    
    echo "Unable to retrieve weather for: $location"
    return 1
}

# Call the function with the provided argument
query_china_weather "$1"