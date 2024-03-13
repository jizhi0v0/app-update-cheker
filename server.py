from fastapi import FastAPI, HTTPException, Query
import json
import os
from colorama import init
from interface.implements.AppStore.AppStoreStrategy import AppStoreStrategy
from interface.implements.Brew.BrewStrategy import BrewStrategy
from interface.implements.DingTalk.DingTalkStrategy import DingTalkStrategy
from lib import checkutil, apputil
from interface.AppVersionStrategy import get_app_info
from lib.apputil import generate_url, get_final_url
from type.index import OldVersionInfo

app = FastAPI()

# 初始化Colorama
init(autoreset=True)

# 应用基础路径
basePath = '/Applications/'
# 加载配置
with open('config/skip_list.json', 'r') as file:
    skip_list = json.load(file)

with open('config/app_to_link_mapping_appstore.json', 'r') as file:
    app_to_link_mapping = json.load(file)

with open('config/app_to_link_mapping_official.json', 'r') as file:
    app_to_link_official_mapping = json.load(file)

with open('config/app_to_link_mapping_brew.json', 'r') as file:
    app_to_link_brew_mapping = json.load(file)


@app.get("/check_updates/")
async def get_app_updates(app_name: str = Query(None, title="App Name", description="The name of the app to check updates for.")):
    file_list = [file for file in os.listdir(basePath) if file.endswith('.app') and file.replace('.app', '') not in skip_list]
    if app_name:
        if app_name + '.app' not in file_list:
            raise HTTPException(status_code=404, detail="App not found")
        file_list = [app_name + '.app']

    update_info_list = []

    for file in file_list:
        app_update_info = check_app_updates(file)
        if app_update_info:
            update_info_list.append(app_update_info)

    return update_info_list


def check_app_updates(file_name: str):
    global old_version_info
    app_name = file_name.replace('.app', '')
    content_path = os.path.join(basePath, file_name, 'Contents')
    wrapper_content = os.path.join(basePath, file_name, 'Wrapper')
    is_app_store_app = checkutil.is_appstore_app(content_path)
    is_wrapper_app = checkutil.is_wrapper_app(basePath + file_name)

    plist_json = apputil.read_info_plist(content_path, 'Info.plist')
    wrapper_json = apputil.read_info_plist(wrapper_content, 'iTunesMetadata.plist')
    old_version = "unknown_version"
    if plist_json is not None:
        old_version = plist_json.get('CFBundleShortVersionString', plist_json.get('CFBundleVersion', 'unknown_version'))
    elif wrapper_json:
        old_version = wrapper_json.get('bundleShortVersionString', 'unknown_version')

    strategy = None
    link = None
    compare_version = old_version
    if is_app_store_app or is_wrapper_app:
        if app_name in app_to_link_mapping:
            strategy = AppStoreStrategy()
            link = app_to_link_mapping[app_name]
    else:
        if app_name in app_to_link_official_mapping:
            link = app_to_link_official_mapping[app_name]
            if "DingTalk" in app_name:
                strategy = DingTalkStrategy()
                compare_version = plist_json.get("buildNo")
        elif app_name in app_to_link_brew_mapping:
            strategy = BrewStrategy()
            link = app_to_link_brew_mapping[app_name]
        else:
            final_url = generate_url(app_name)
            url_info = get_final_url(final_url)
            if url_info:
                strategy = BrewStrategy()
                link = final_url

    if strategy:
        old_version_info = OldVersionInfo(showVersion=old_version, compareVersion=compare_version, appName=app_name)
        app_info = get_app_info(link=link, old_version_info=old_version_info, strategy=strategy)
        if app_info.needUpdate:
            return {
                "app_name": app_name,
                "current_version": old_version,
                "latest_version": app_info.latestVersion,
                "update_required": True,
                "download_url": app_info.downloadUrl,
            }
        else:
            return {
                "app_name": app_name,
                "current_version": old_version,
                "update_required": False,
            }
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
