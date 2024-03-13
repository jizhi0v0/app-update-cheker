from interface.AppVersionStrategy import AppVersionStrategy
from lib.apputil import get_final_url
from type.index import AppStoreAppInfo
import re


class DingTalkStrategy(AppVersionStrategy):
    def get_version_info(self, link, old_version_info) -> "AppStoreAppInfo":
        # 实现从Google Play获取版本信息的逻辑

        url_info = get_final_url(link)

        match = re.search(r'(\d+)_universal\.dmg$', url_info.realDownloadUrl)

        version_key = match.group(1) if match else None
        return AppStoreAppInfo(old_version_info.showVersion, version_key, url_info.lastModified,
                               url_info.realDownloadUrl,
                               version_key != old_version_info.compareVersion)
