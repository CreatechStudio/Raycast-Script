#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Get Bundle ID
# @raycast.mode inline
# @raycast.packageName get-bundle-id
# @raycast.refreshTime 3s

# Optional parameters:
# @raycast.icon images/appstore-icon.png

# Documentation:
# @raycast.description Get Bundle ID

# 安装依赖
import importlib
import pip
depends = [
    ('requests', 'requests'),
    ('pyperclip', 'PaperClip')
]
for pack_name, imp_name in depends:
    try:
        importlib.import_module(imp_name)
    except:
        pip.main(['install', pack_name])


import requests
import re
import subprocess
import sys
import pyperclip


def extract_app_id(url):
    pattern = r'id(\d+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def fetch_data(app_id, url):
    lookup_url = f'https://itunes.apple.com/{url}/lookup?id={app_id}'
    response = requests.get(lookup_url)
    if response.status_code == 200:
        return response.json()
    return None

def extract_bundle_id(data):
    if data and 'results' in data and len(data['results']) > 0:
        return data['results'][0].get('bundleId')
    return None

def copy_to_clipboard(text):
    subprocess.run(['pbcopy'], universal_newlines=True, input=text)

def save_bundle_id_from_app_store_link():
    clipboard_content = pyperclip.paste()
    app_store_link = clipboard_content.strip()

    if app_store_link:
        app_id = extract_app_id(app_store_link)

        if app_id:
            json_data = fetch_data(app_id, 'cn')
            bundle_id = extract_bundle_id(json_data)

            if bundle_id:
                copy_to_clipboard(bundle_id)
                print(f"已复制 {bundle_id} 已复制到剪贴板")
            else:
                json_data = fetch_data(app_id, 'us')
                bundle_id = extract_bundle_id(json_data)

                if bundle_id:
                    copy_to_clipboard(bundle_id)
                    print(f"已复制 {bundle_id} 已复制到剪贴板")
                else:
                    print("无法获取 bundleId。")
        else:
            print("无法提取 App ID。")
    else:
        print("剪贴板中未找到 App Store 链接。")

if __name__ == "__main__":
    save_bundle_id_from_app_store_link()