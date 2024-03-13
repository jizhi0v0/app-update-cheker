import json
import os

from interface.implements.AppStore.AppStoreStrategy import AppStoreStrategy
from interface.implements.DingTalk.DingTalkStrategy import DingTalkStrategy
from lib import checkutil
from lib import apputil
from interface.AppVersionStrategy import get_app_info
from type.index import OldVersionInfo

basePath = '/Applications/'
file_list = os.listdir(basePath)

with open('config/skip_list.json', 'r') as skip_list_file:
    skip_list = json.load(skip_list_file)

with open('config/app_to_link_mapping_appstore.json', 'r') as app_to_link_file:
    app_to_link_mapping = json.load(app_to_link_file)

with open('config/app_to_link_mapping_official.json', 'r') as app_to_link_official_file:
    app_to_link_official_mapping = json.load(app_to_link_official_file)

for file in file_list:
    if file in skip_list:
        continue

    content_path = os.path.join(basePath, file, 'Contents')
    wrapper_content = os.path.join(basePath, file, 'Wrapper')
    is_app_store_app = checkutil.is_appstore_app(content_path)
    is_wrapper_app = checkutil.is_wrapper_app(basePath + file)

    app_name = file.replace('.app', '')
    plist_json = apputil.read_info_plist(content_path, 'Info.plist')
    wrapper_json = apputil.read_info_plist(wrapper_content, 'iTunesMetadata.plist')
    if plist_json is not None:
        old_version = plist_json.get('CFBundleShortVersionString', 'unknown_version')
    else:
        old_version = wrapper_json.get('bundleShortVersionString', 'unknown_version')

    old_version_info = None
    strategy = None
    link = None
    if is_app_store_app or is_wrapper_app:
        if app_name in app_to_link_mapping:
            strategy = AppStoreStrategy()
            old_version_info = OldVersionInfo(showVersion=old_version, compareVersion=old_version)
            link = app_to_link_mapping[app_name]
    else:
        if app_name in app_to_link_official_mapping:
            if "DingTalk" in app_name:
                strategy = DingTalkStrategy()
                compare_version = plist_json.get("buildNo")
                old_version_info = OldVersionInfo(showVersion=old_version, compareVersion=compare_version)
                link = app_to_link_official_mapping[app_name]
        else:
            print(app_name, 'wait for support')

    if strategy is not None and old_version_info is not None and link is not None:
        app_info = get_app_info(link=link, old_version_info=old_version_info,
                                strategy=strategy)
        print(app_name, 'need update, the latest version is ' + app_info.latestVersion
                        if app_info.needUpdate else "don't need update",
                        ', your version is ' + app_info.oldVersion, app_info)
