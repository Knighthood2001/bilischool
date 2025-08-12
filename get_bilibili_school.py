import requests
import re
import json

def get_up_school_info(uid):
    url = f"https://m.bilibili.com/space/{uid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        'Referer': "https://www.bilibili.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
    
    try:
        # 获取用户主页HTML
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        # print(html_content)

        # 使用正则表达式提取JSON数据
        pattern = r'window\.__INITIAL_STATE__=(.*?);\(function\(\)'
        match = re.search(pattern, html_content)
        if not match:
            print("未找到用户数据")
            return None
            
        # 解析JSON数据
        json_str = match.group(1)
        user_data = json.loads(json_str)
        # print(user_data)
        
        # 从JSON中提取学校信息
        if "space" in user_data and "info" in user_data["space"] and "school" in user_data["space"]["info"]:
            school_info = user_data["space"]["info"]["school"].get("name")
            if school_info:
                return school_info
        
        return None
        
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"数据解析失败: {e}")
        return None

# 示例使用
if __name__ == "__main__":
    # uid = "395939636"  # 测试UID：华东理工大学
    uid = "245645656"  # 测试UID：清华大学
    school_info = get_up_school_info(uid)
    
    if school_info:
        print(f"该UP主的学校: {school_info}")
    else:
        print("未找到该UP主的学校信息")