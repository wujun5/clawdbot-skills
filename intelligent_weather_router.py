#!/usr/bin/env python3
"""
智能回退版中国天气查询脚本（集成地理信息补全功能）
当无法查询到具体城市时，自动回退到省级或附近城市
"""

import requests
import json
import sys
import urllib.parse
import re
from typing import Optional, Tuple
import os

class GeoInfoCompleter:
    def __init__(self):
        # 地理层级关系映射
        self.administrative_hierarchy = {
            # 直辖市
            "北京": ["北京市"],
            "上海": ["上海市"],
            "天津": ["天津市"],
            "重庆": ["重庆市"],
            
            # 浙江省
            "杭州": ["浙江省", "杭州市"],
            "宁波": ["浙江省", "宁波市"],
            "温州": ["浙江省", "温州市"],
            "嘉兴": ["浙江省", "嘉兴市"],
            "湖州": ["浙江省", "湖州市"],
            "绍兴": ["浙江省", "绍兴市"],
            "金华": ["浙江省", "金华市"],
            "衢州": ["浙江省", "衢州市"],
            "舟山": ["浙江省", "舟山市"],
            "台州": ["浙江省", "台州市"],
            "丽水": ["浙江省", "丽水市"],
            
            # 江西省
            "南昌": ["江西省", "南昌市"],
            "景德镇": ["江西省", "景德镇市"],
            "萍乡": ["江西省", "萍乡市"],
            "九江": ["江西省", "九江市"],
            "新余": ["江西省", "新余市"],
            "鹰潭": ["江西省", "鹰潭市"],
            "赣州": ["江西省", "赣州市"],
            "吉安": ["江西省", "吉安市"],
            "宜春": ["江西省", "宜春市"],
            "抚州": ["江西省", "抚州市"],
            "上饶": ["江西省", "上饶市"],
            
            # 江苏省
            "南京": ["江苏省", "南京市"],
            "无锡": ["江苏省", "无锡市"],
            "徐州": ["江苏省", "徐州市"],
            "常州": ["江苏省", "常州市"],
            "苏州": ["江苏省", "苏州市"],
            "南通": ["江苏省", "南通市"],
            "连云港": ["江苏省", "连云港市"],
            "淮安": ["江苏省", "淮安市"],
            "盐城": ["江苏省", "盐城市"],
            "扬州": ["江苏省", "扬州市"],
            "镇江": ["江苏省", "镇江市"],
            "泰州": ["江苏省", "泰州市"],
            "宿迁": ["江苏省", "宿迁市"],
            
            # 广东省
            "广州": ["广东省", "广州市"],
            "深圳": ["广东省", "深圳市"],
            "珠海": ["广东省", "珠海市"],
            "汕头": ["广东省", "汕头市"],
            "佛山": ["广东省", "佛山市"],
            "韶关": ["广东省", "韶关市"],
            "湛江": ["广东省", "湛江市"],
            "肇庆": ["广东省", "肇庆市"],
            "江门": ["广东省", "江门市"],
            "茂名": ["广东省", "茂名市"],
            "惠州": ["广东省", "惠州市"],
            "梅州": ["广东省", "梅州市"],
            "汕尾": ["广东省", "汕尾市"],
            "河源": ["广东省", "河源市"],
            "阳江": ["广东省", "阳江市"],
            "清远": ["广东省", "清远市"],
            "东莞": ["广东省", "东莞市"],
            "中山": ["广东省", "中山市"],
            "潮州": ["广东省", "潮州市"],
            "揭阳": ["广东省", "揭阳市"],
            "云浮": ["广东省", "云浮市"],
            
            # 福建省
            "福州": ["福建省", "福州市"],
            "厦门": ["福建省", "厦门市"],
            "莆田": ["福建省", "莆田市"],
            "三明": ["福建省", "三明市"],
            "泉州": ["福建省", "泉州市"],
            "漳州": ["福建省", "漳州市"],
            "南平": ["福建省", "南平市"],
            "龙岩": ["福建省", "龙岩市"],
            "宁德": ["福建省", "宁德市"],
            
            # 湖南省
            "长沙": ["湖南省", "长沙市"],
            "株洲": ["湖南省", "株洲市"],
            "湘潭": ["湖南省", "湘潭市"],
            "衡阳": ["湖南省", "衡阳市"],
            "邵阳": ["湖南省", "邵阳市"],
            "岳阳": ["湖南省", "岳阳市"],
            "常德": ["湖南省", "常德市"],
            "张家界": ["湖南省", "张家界市"],
            "益阳": ["湖南省", "益阳市"],
            "郴州": ["湖南省", "郴州市"],
            "永州": ["湖南省", "永州市"],
            "怀化": ["湖南省", "怀化市"],
            "娄底": ["湖南省", "娄底市"],
            "湘西": ["湖南省", "湘西土家族苗族自治州"],
            
            # 湖北省
            "武汉": ["湖北省", "武汉市"],
            "黄石": ["湖北省", "黄石市"],
            "十堰": ["湖北省", "十堰市"],
            "宜昌": ["湖北省", "宜昌市"],
            "襄阳": ["湖北省", "襄阳市"],
            "鄂州": ["湖北省", "鄂州市"],
            "荆门": ["湖北省", "荆门市"],
            "孝感": ["湖北省", "孝感市"],
            "荆州": ["湖北省", "荆州市"],
            "黄冈": ["湖北省", "黄冈市"],
            "咸宁": ["湖北省", "咸宁市"],
            "随州": ["湖北省", "随州市"],
            "恩施": ["湖北省", "恩施土家族苗族自治州"],
            
            # 安徽省
            "合肥": ["安徽省", "合肥市"],
            "芜湖": ["安徽省", "芜湖市"],
            "蚌埠": ["安徽省", "蚌埠市"],
            "淮南": ["安徽省", "淮南市"],
            "马鞍山": ["安徽省", "马鞍山市"],
            "淮北": ["安徽省", "淮北市"],
            "铜陵": ["安徽省", "铜陵市"],
            "安庆": ["安徽省", "安庆市"],
            "黄山": ["安徽省", "黄山市"],
            "滁州": ["安徽省", "滁州市"],
            "阜阳": ["安徽省", "阜阳市"],
            "宿州": ["安徽省", "宿州市"],
            "六安": ["安徽省", "六安市"],
            "亳州": ["安徽省", "亳州市"],
            "池州": ["安徽省", "池州市"],
            "宣城": ["安徽省", "宣城市"],
            
            # 四川省
            "成都": ["四川省", "成都市"],
            "自贡": ["四川省", "自贡市"],
            "攀枝花": ["四川省", "攀枝花市"],
            "泸州": ["四川省", "泸州市"],
            "德阳": ["四川省", "德阳市"],
            "绵阳": ["四川省", "绵阳市"],
            "广元": ["四川省", "广元市"],
            "遂宁": ["四川省", "遂宁市"],
            "内江": ["四川省", "内江市"],
            "乐山": ["四川省", "乐山市"],
            "南充": ["四川省", "南充市"],
            "眉山": ["四川省", "眉山市"],
            "宜宾": ["四川省", "宜宾市"],
            "广安": ["四川省", "广安市"],
            "达州": ["四川省", "达州市"],
            "雅安": ["四川省", "雅安市"],
            "巴中": ["四川省", "巴中市"],
            "资阳": ["四川省", "资阳市"],
            "阿坝": ["四川省", "阿坝藏族羌族自治州"],
            "甘孜": ["四川省", "甘孜藏族自治州"],
            "凉山": ["四川省", "凉山彝族自治州"],
        }
        
        # 县级市映射
        self.county_cities = {
            # 浙江省
            "萧山": ["浙江省", "杭州市", "萧山区"],
            "余杭": ["浙江省", "杭州市", "余杭区"],
            "富阳": ["浙江省", "杭州市", "富阳区"],
            "临安": ["浙江省", "杭州市", "临安区"],
            "慈溪": ["浙江省", "宁波市", "慈溪市"],
            "余姚": ["浙江省", "宁波市", "余姚市"],
            "奉化": ["浙江省", "宁波市", "奉化区"],
            "象山": ["浙江省", "宁波市", "象山县"],
            "宁海": ["浙江省", "宁波市", "宁海县"],
            "瑞安": ["浙江省", "温州市", "瑞安市"],
            "乐清": ["浙江省", "温州市", "乐清市"],
            "永嘉": ["浙江省", "温州市", "永嘉县"],
            "平阳": ["浙江省", "温州市", "平阳县"],
            "苍南": ["浙江省", "温州市", "苍南县"],
            "文成": ["浙江省", "温州市", "文成县"],
            "泰顺": ["浙江省", "温州市", "泰顺县"],
            "洞头": ["浙江省", "温州市", "洞头区"],
            "海宁": ["浙江省", "嘉兴市", "海宁市"],
            "平湖": ["浙江省", "嘉兴市", "平湖市"],
            "桐乡": ["浙江省", "嘉兴市", "桐乡市"],
            "嘉善": ["浙江省", "嘉兴市", "嘉善县"],
            "海盐": ["浙江省", "嘉兴市", "海盐县"],
            "德清": ["浙江省", "湖州市", "德清县"],
            "长兴": ["浙江省", "湖州市", "长兴县"],
            "安吉": ["浙江省", "湖州市", "安吉县"],
            "诸暨": ["浙江省", "绍兴市", "诸暨市"],
            "嵊州": ["浙江省", "绍兴市", "嵊州市"],
            "新昌": ["浙江省", "绍兴市", "新昌县"],
            "义乌": ["浙江省", "金华市", "义乌市"],
            "东阳": ["浙江省", "金华市", "东阳市"],
            "永康": ["浙江省", "金华市", "永康市"],
            "兰溪": ["浙江省", "金华市", "兰溪市"],
            "浦江": ["浙江省", "金华市", "浦江县"],
            "磐安": ["浙江省", "金华市", "磐安县"],
            "武义": ["浙江省", "金华市", "武义县"],
            "江山": ["浙江省", "衢州市", "江山市"],
            "常山": ["浙江省", "衢州市", "常山县"],
            "开化": ["浙江省", "衢州市", "开化县"],
            "龙游": ["浙江省", "衢州市", "龙游县"],
            "岱山": ["浙江省", "舟山市", "岱山县"],
            "嵊泗": ["浙江省", "舟山市", "嵊泗县"],
            "临海": ["浙江省", "台州市", "临海市"],
            "温岭": ["浙江省", "台州市", "温岭市"],
            "玉环": ["浙江省", "台州市", "玉环市"],
            "天台": ["浙江省", "台州市", "天台县"],
            "仙居": ["浙江省", "台州市", "仙居县"],
            "三门": ["浙江省", "台州市", "三门县"],
            "龙泉": ["浙江省", "丽水市", "龙泉市"],
            "青田": ["浙江省", "丽水市", "青田县"],
            "缙云": ["浙江省", "丽水市", "缙云县"],
            "遂昌": ["浙江省", "丽水市", "遂昌县"],
            "松阳": ["浙江省", "丽水市", "松阳县"],
            "云和": ["浙江省", "丽水市", "云和县"],
            "庆元": ["浙江省", "丽水市", "庆元县"],
            "景宁": ["浙江省", "丽水市", "景宁县"],
            
            # 江西省
            "瑞昌": ["江西省", "九江市", "瑞昌市"],
            "共青城": ["江西省", "九江市", "共青城市"],
            "庐山": ["江西省", "九江市", "庐山市"],
            "乐平": ["江西省", "景德镇市", "乐平市"],
            "瑞金": ["江西省", "赣州市", "瑞金市"],
            "南康": ["江西省", "赣州市", "南康区"],
            "德兴": ["江西省", "上饶市", "德兴市"],
            "玉山": ["江西省", "上饶市", "玉山县"],
            "广丰": ["江西省", "上饶市", "广丰区"],
            "铅山": ["江西省", "上饶市", "铅山县"],
            "横峰": ["江西省", "上饶市", "横峰县"],
            "弋阳": ["江西省", "上饶市", "弋阳县"],
            "余干": ["江西省", "上饶市", "余干县"],
            "鄱阳": ["江西省", "上饶市", "鄱阳县"],
            "万年": ["江西省", "上饶市", "万年县"],
            "婺源": ["江西省", "上饶市", "婺源县"],
            "德安": ["江西省", "九江市", "德安县"],
            "星子": ["江西省", "九江市", "庐山市"],
        }

    def complete_geo_info(self, location: str) -> Tuple[str, str, str]:
        """
        补全地理位置信息
        返回: (省份, 城市, 区县)
        """
        # 检查是否是县级市
        for county, hierarchy in self.county_cities.items():
            if county in location:
                return tuple(hierarchy)
        
        # 检查是否是地级市
        for city, hierarchy in self.administrative_hierarchy.items():
            if city in location:
                if len(hierarchy) == 1:  # 直辖市
                    return hierarchy[0], hierarchy[0], hierarchy[0]
                elif len(hierarchy) == 2:  # 省市
                    return hierarchy[0], hierarchy[1], hierarchy[1]
        
        # 如果无法匹配，尝试从输入中提取信息
        province = None
        city = None
        district = None
        
        # 尝试匹配省份
        provinces = [
            '北京', '上海', '天津', '重庆',
            '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
            '江苏', '浙江', '安徽', '福建', '江西', '山东',
            '河南', '湖北', '湖南', '广东', '广西', '海南',
            '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆'
        ]
        
        for prov in provinces:
            if prov in location:
                province = prov
                break
        
        # 尝试匹配城市
        cities = list(self.administrative_hierarchy.keys())
        for cit in cities:
            if cit in location and province:
                # 确保城市属于该省份
                hierarchy = self.administrative_hierarchy[cit]
                if province in hierarchy[0] if isinstance(hierarchy[0], str) else province in hierarchy:
                    city = cit
                    break
        
        # 如果城市未找到，尝试从县级市中查找
        if not city:
            for county in self.county_cities:
                if county in location and province:
                    hierarchy = self.county_cities[county]
                    if province == hierarchy[0]:
                        city = hierarchy[1]  # 使用所属的地级市
                        district = hierarchy[2]
                        break
        
        # 构造返回值
        if district:
            return province or "", city or "", district
        elif city:
            return province or "", city, city
        else:
            return province or "", location, location

    def normalize_location(self, location: str) -> str:
        """
        标准化位置名称，去除冗余词汇
        """
        # 去除常见的后缀词
        location = re.sub(r'(市|县|区|省)$', '', location)
        
        # 处理一些常见的别名
        aliases = {
            '京': '北京',
            '沪': '上海',
            '津': '天津',
            '渝': '重庆',
        }
        
        for alias, full_name in aliases.items():
            if alias == location:
                return full_name
        
        return location

def load_city_codes():
    """加载城市代码"""
    # 尝试多个可能的路径
    possible_paths = [
        '/home/Tim/BotRoom/complete_china_weather_city_codes.json',
        '/home/Tim/BotRoom/clawdbot-skills/scripts/complete_china_weather_city_codes.json',
        '/home/Tim/BotRoom/skills_workspace/china-weather/scripts/complete_china_weather_city_codes.json',
        './complete_china_weather_city_codes.json'
    ]

    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    print(f"从 {path} 加载了 {len(json.load(f))} 个城市代码")
                    f.seek(0)  # 重置文件指针
                    return json.load(f)
        except FileNotFoundError:
            continue
    
    # 如果没有找到完整文件，使用备用字典
    backup_codes = {
        "北京": "101010100", "上海": "101020100", "广州": "101280101", "深圳": "101280601",
        "杭州": "101210101", "南京": "101190101", "武汉": "101200101", "成都": "101270101",
        "重庆": "101040100", "西安": "101110101", "天津": "101030100", "苏州": "101190401",
        "青岛": "101120201", "大连": "101070201", "厦门": "101230201", "宁波": "101210401",
        "长沙": "101250101", "郑州": "101180101", "济南": "101120101", "福州": "101230101",
        "南昌": "101240101", "沈阳": "101060101", "哈尔滨": "101050101", "石家庄": "101090101",
        "太原": "101100101", "昆明": "101290101", "南宁": "101300101", "合肥": "101220101",
        "海口": "101310101", "兰州": "101160101", "银川": "101170101", "西宁": "101150101",
        "拉萨": "101140101", "乌鲁木齐": "101130101", "呼和浩特": "101080101", "长春": "101060201",
        "唐山": "101090301", "秦皇岛": "101091101", "邯郸": "101090402", "保定": "101090201",
        "张家口": "101090301", "承德": "101090402", "沧州": "101090701", "廊坊": "101090601",
        "衡水": "101090801", "邢台": "101090901", "晋城": "101100601", "朔州": "101100901",
        "忻州": "101101001", "大同": "101100201", "阳泉": "101100301", "长治": "101100501",
        "临汾": "101100701", "吕梁": "101101100", "运城": "101100801", "鞍山": "101070101",
        "抚顺": "101070101", "本溪": "101070101", "丹东": "101070201", "锦州": "101070101",
        "营口": "101070201", "阜新": "101070101", "辽阳": "101070101", "盘锦": "101070401",
        "铁岭": "101070201", "朝阳": "101070101", "葫芦岛": "101070101", "吉林": "101060301",
        "四平": "101060201", "辽源": "101060201", "通化": "101060501", "白山": "101060901",
        "松原": "101060701", "白城": "101060601", "延边": "101060801", "齐齐哈尔": "101050201",
        "鸡西": "101050301", "鹤岗": "101050301", "双鸭山": "101050301", "大庆": "101050901",
        "伊春": "101050801", "牡丹江": "101050301", "佳木斯": "101050401", "七台河": "101050301",
        "黑河": "101050601", "绥化": "101050501", "大兴安岭": "101050701"
    }
    print("警告: 未能加载完整城市代码文件，使用备用字典")
    return backup_codes

def load_province_codes():
    """加载省份代码"""
    # 尝试多个可能的路径
    possible_paths = [
        '/home/Tim/BotRoom/china_weather_province_codes.json',
        '/home/Tim/BotRoom/clawdbot-skills/scripts/china_weather_province_codes.json',
        '/home/Tim/BotRoom/skills_workspace/china-weather/scripts/china_weather_province_codes.json',
        './china_weather_province_codes.json'
    ]

    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except FileNotFoundError:
            continue
    
    # 如果没有找到省份代码文件，返回空字典
    return {}

def find_city_code(city_name: str, city_codes: dict, province_codes: dict):
    """查找城市代码，支持城市名和省份+城市名的组合"""
    # 首先尝试精确匹配城市名
    if city_name in city_codes:
        return city_codes[city_name]
    
    # 如果找不到，尝试查找包含该城市名的条目
    for name, code in city_codes.items():
        if city_name in name or name in city_name:
            return code
    
    # 如果输入包含省份信息，尝试解析
    for prov_name in province_codes:
        if city_name.startswith(prov_name):
            # 提取城市名部分
            city_part = city_name[len(prov_name):]
            if city_part:  # 如果还有剩余部分
                # 查找以该省份代码开头且包含城市名部分的城市
                prov_code_prefix = province_codes[prov_name]['code']
                for name, code in city_codes.items():
                    if code.startswith(prov_code_prefix) and city_part in name:
                        return code
    
    return None

def get_province_from_city_code(city_code: str, province_codes: dict):
    """从城市代码推断省份代码"""
    if len(city_code) >= 5:
        prov_code_prefix = city_code[:5]
        for prov_name, prov_info in province_codes.items():
            if prov_info['code'] == prov_code_prefix:
                return prov_name
    return None

def find_cities_by_province(province_name: str, city_codes: dict, province_codes: dict):
    """查找省份下的所有城市"""
    if province_name not in province_codes:
        return []
    
    prov_code = province_codes[province_name]['code']
    province_cities = []
    
    for city_name, city_code in city_codes.items():
        if city_code.startswith(prov_code):
            province_cities.append((city_name, city_code))
    
    return province_cities

def query_weather_com_cn_api_v2(city_code: str) -> Optional[str]:
    """
    使用中国天气网API v2版本
    """
    try:
        # 尝试使用新的API端点
        url = f"http://d1.weather.com.cn/weather_index/{city_code}.shtml"
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            # 尝试解析返回的JSON数据
            try:
                # 查找JSON数据部分
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_part = content[start:end]
                    # 尝试解析为JSON
                    data = json.loads(json_part)
                    
                    # 根据可能的字段名提取数据
                    city = data.get('city', '未知城市')
                    temp = data.get('temp', data.get('real', {}).get('temp', '未知'))
                    weather = data.get('weather', data.get('real', {}).get('weather', '未知'))
                    
                    return f"{city}: {weather} {temp}°C"
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试正则表达式解析
                temp_match = re.search(r'"temp":"([^"]*)"', content)
                weather_match = re.search(r'"weather":"([^"]*)"', content)
                city_match = re.search(r'"city":"([^"]*)"', content)
                
                if temp_match:
                    temp = temp_match.group(1)
                    weather = weather_match.group(1) if weather_match else "天气"
                    city = city_match.group(1) if city_match else "城市"
                    return f"{city}: {weather} {temp}°C"
        
        return None
    except Exception as e:
        print(f"API v2查询失败: {e}", file=sys.stderr)
        return None

def query_weather_com_cn_api_v1(city_code: str) -> Optional[str]:
    """
    使用中国天气网API v1版本（备用）
    """
    try:
        # 尝试使用旧的API端点
        url = f"http://www.weather.com.cn/data/sk/{city_code}.html"
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                real_data = data.get('data', {}).get('real', {})
                
                if real_data:
                    city = real_data.get('city', '未知城市')
                    temp = real_data.get('temp', '未知')
                    weather = real_data.get('weather', '未知')
                    
                    return f"{city}: {weather} {temp}°C"
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试正则表达式
                content = response.text
                temp_match = re.search(r'"temp":"([^"]*)"', content)
                weather_match = re.search(r'"weather":"([^"]*)"', content)
                city_match = re.search(r'"city":"([^"]*)"', content)
                
                if temp_match:
                    temp = temp_match.group(1)
                    weather = weather_match.group(1) if weather_match else "天气"
                    city = city_match.group(1) if city_match else "城市"
                    return f"{city}: {weather} {temp}°C"
        
        return None
    except Exception as e:
        print(f"API v1查询失败: {e}", file=sys.stderr)
        return None

def query_weather_com_cn(city_name: str) -> Optional[str]:
    """
    查询中国天气网API，支持城市代码和省份代码
    """
    # 加载城市和省份代码
    city_codes = load_city_codes()
    province_codes = load_province_codes()
    
    # 查找城市代码
    city_code = find_city_code(city_name, city_codes, province_codes)
    
    if not city_code:
        return None
    
    print(f"使用城市代码: {city_code} 查询 {city_name}")
    
    # 首先尝试API v2
    result = query_weather_com_cn_api_v2(city_code)
    if result:
        print("使用中国天气网API v2")
        return result
    
    # 如果v2失败，尝试API v1
    result = query_weather_com_cn_api_v1(city_code)
    if result:
        print("使用中国天气网API v1")
        return result
    
    return None

def query_wttr_in(location: str) -> Optional[str]:
    """
    查询wttr.in服务（备用）
    """
    try:
        import subprocess
        cmd = f'curl -s "wttr.in/{location}?format=3"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            # 简单翻译
            translations = {
                'Clear': '晴', 'Sunny': '晴', 'Partly cloudy': '多云', 
                'Cloudy': '阴', 'Overcast': '阴', 'Rain': '雨',
                'Light rain': '小雨', 'Moderate rain': '中雨', 'Heavy rain': '大雨',
                'Showers': '阵雨', 'Snow': '雪', 'Light snow': '小雪',
                'Moderate snow': '中雪', 'Heavy snow': '大雪', 'Fog': '雾',
                'Thunderstorm': '雷暴'
            }
            
            for eng, chi in translations.items():
                output = output.replace(eng, chi)
            
            return output
    except Exception:
        pass
    return None

def query_openmeteo_by_city(city_name: str) -> Optional[str]:
    """
    通过城市名使用Open-Meteo服务（需要先获取坐标）
    """
    try:
        # 先获取坐标
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city_name)}&format=json&limit=1"
        response = requests.get(geocode_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Clawbot Weather)'})
        
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            lat = float(data['lat'])
            lon = float(data['lon'])
            
            # 查询天气
            meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius&windspeed_unit=kmh"
            weather_response = requests.get(meteo_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                current = weather_data['current_weather']
                
                temp = current['temperature']
                weathercode = current.get('weathercode', 0)
                windspeed = current['windspeed']
                
                # 天气代码映射
                weather_map = {
                    0: '晴', 1: '晴间多云', 2: '阴', 3: '阴',
                    45: '雾', 48: '雾', 51: '小雨', 53: '中雨', 55: '大雨',
                    61: '小雨', 63: '中雨', 65: '大雨', 71: '小雪', 73: '中雪', 75: '大雪',
                    95: '雷暴', 96: '雷暴伴冰雹', 99: '雷暴伴大冰雹'
                }
                
                desc = weather_map.get(weathercode, '天气')
                
                return f"{city_name}: {desc} {temp}°C 风速:{windspeed}km/h"
    except Exception as e:
        print(f"Open-Meteo查询失败: {e}", file=sys.stderr)
    
    return None

def is_china_location(location):
    """
    判断位置是否在中国境内
    """
    # 加载城市代码
    city_codes = load_city_codes()
    
    # 使用所有城市名称作为关键词
    china_keywords = list(city_codes.keys())
    
    # 检查是否包含中国关键词
    location_lower = location.lower()
    for keyword in china_keywords:
        if keyword.lower() in location_lower:
            return True
    
    # 检查是否以中国开头或结尾
    if '中国' in location or 'China' in location_lower:
        return True
    
    # 检查省份关键词
    provinces = [
        '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', 
        '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', 
        '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', 
        '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '香港', '澳门'
    ]
    
    for prov in provinces:
        if prov in location:
            return True
    
    return False

def query_fallback_weather(location: str) -> str:
    """
    智能回退天气查询
    当无法查询到具体城市时，自动回退到省级或附近城市
    """
    city_codes = load_city_codes()
    province_codes = load_province_codes()
    
    # 首先尝试直接查询
    direct_result = query_weather_com_cn(location)
    if direct_result:
        return direct_result
    
    # 如果直接查询失败，尝试wttr.in
    wttr_result = query_wttr_in(location)
    if wttr_result:
        return wttr_result
    
    # 如果城市名查询失败，尝试提取省份信息并查询省会
    for prov_name in province_codes:
        if location.startswith(prov_name):
            # 如果是省份+城市的形式，尝试查询省会
            capital_mapping = {
                '北京': '北京', '上海': '上海', '天津': '天津', '重庆': '重庆',
                '河北': '石家庄', '山西': '太原', '内蒙古': '呼和浩特',
                '辽宁': '沈阳', '吉林': '长春', '黑龙江': '哈尔滨',
                '江苏': '南京', '浙江': '杭州', '安徽': '合肥', '福建': '福州', '江西': '南昌', '山东': '济南',
                '河南': '郑州', '湖北': '武汉', '湖南': '长沙',
                '广东': '广州', '广西': '南宁', '海南': '海口',
                '四川': '成都', '贵州': '贵阳', '云南': '昆明',
                '西藏': '拉萨', '陕西': '西安', '甘肃': '兰州', '青海': '西宁', '宁夏': '银川', '新疆': '乌鲁木齐'
            }
            
            if prov_name in capital_mapping:
                capital = capital_mapping[prov_name]
                print(f"未找到 {location} 的具体天气，回退到查询 {prov_name} 省会 {capital}")
                result = query_weather_com_cn(capital)
                if result:
                    return f"[{location} 天气暂无，显示{prov_name}省会] {result}"
                
                # 如果省会也查不到，尝试wttr.in
                result = query_wttr_in(capital)
                if result:
                    return f"[{location} 天气暂无，显示{prov_name}省会] {capital}: {result}"
    
    # 如果是具体城市名但没查到，尝试查找相近的城市
    for city_name in city_codes:
        if location in city_name or city_name in location:
            print(f"未找到 {location} 的具体天气，回退到查询相近城市 {city_name}")
            result = query_weather_com_cn(city_name)
            if result:
                return f"[{location} 天气暂无，显示相近城市] {result}"
    
    # 如果以上都失败，尝试Open-Meteo
    openmeteo_result = query_openmeteo_by_city(location)
    if openmeteo_result:
        return openmeteo_result
    
    # 最后的回退：尝试查询省份
    for prov_name in province_codes:
        if prov_name in location:
            capital_mapping = {
                '北京': '北京', '上海': '上海', '天津': '天津', '重庆': '重庆',
                '河北': '石家庄', '山西': '太原', '内蒙古': '呼和浩特',
                '辽宁': '沈阳', '吉林': '长春', '黑龙江': '哈尔滨',
                '江苏': '南京', '浙江': '杭州', '安徽': '合肥', '福建': '福州', '江西': '南昌', '山东': '济南',
                '河南': '郑州', '湖北': '武汉', '湖南': '长沙',
                '广东': '广州', '广西': '南宁', '海南': '海口',
                '四川': '成都', '贵州': '贵阳', '云南': '昆明',
                '西藏': '拉萨', '陕西': '西安', '甘肃': '兰州', '青海': '西宁', '宁夏': '银川', '新疆': '乌鲁木齐'
            }
            
            if prov_name in capital_mapping:
                capital = capital_mapping[prov_name]
                print(f"未找到 {location} 的具体天气，回退到查询 {prov_name} 省份天气")
                result = query_wttr_in(capital)
                if result:
                    return f"[{location} 天气暂无，显示{prov_name}] {capital}: {result}"
    
    return f"无法获取 {location} 的天气信息，建议尝试查询省会城市或邻近城市"

def enhance_weather_query_with_geo_completion(original_location: str) -> str:
    """
    结合地理信息补全的天气查询
    """
    completer = GeoInfoCompleter()
    
    # 补全地理信息
    province, city, district = completer.complete_geo_info(original_location)
    
    # 标准化城市名
    normalized_city = completer.normalize_location(city)
    
    print(f"原始查询: {original_location}")
    print(f"补全信息: 省份={province}, 城市={normalized_city}, 区县={district}")
    
    # 返回最合适的查询位置
    if district and district != normalized_city and district in ['江山市', '玉山县']:
        # 对于县级市，如果存在于我们的数据库中，优先使用
        if district in load_city_codes():
            return district
        else:
            # 否则使用所属的地级市
            return normalized_city
    elif normalized_city:
        # 否则使用标准化的城市名
        return normalized_city
    else:
        # 最后使用原始位置
        return original_location

def query_china_weather(location: str) -> str:
    """
    综合查询中国天气（带智能回退和地理信息补全）
    """
    print(f"正在查询: {location}")
    
    # 使用地理信息补全功能增强查询
    enhanced_location = enhance_weather_query_with_geo_completion(location)
    if enhanced_location != location:
        print(f"位置信息已增强，使用: {enhanced_location}")
    
    if is_china_location(enhanced_location):
        print("检测到中国境内位置，使用中国天气服务...")
        return query_fallback_weather(enhanced_location)
    else:
        print("检测到境外位置，使用国际天气服务...")
        # 尝试wttr.in
        result = query_wttr_in(enhanced_location)
        if result:
            print("使用wttr.in服务")
            return result
        
        # 如果wttr.in失败，尝试Open-Meteo
        result = query_openmeteo_by_city(enhanced_location)
        if result:
            print("使用Open-Meteo服务")
            return result
        
        return f"无法获取 {enhanced_location} 的天气信息"

def main():
    if len(sys.argv) < 2:
        print("使用方法: python enhanced_weather_with_geo_completion.py <城市名称>")
        print("示例: python enhanced_weather_with_geo_completion.py 北京")
        print("示例: python enhanced_weather_with_geo_completion.py 浙江嘉兴")
        print("示例: python enhanced_weather_with_geo_completion.py 江西玉山")
        print("示例: python enhanced_weather_with_geo_completion.py 浙江江山")
        return
    
    location = sys.argv[1]
    result = query_china_weather(location)
    print(result)

if __name__ == "__main__":
    main()