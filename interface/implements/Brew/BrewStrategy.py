import json

import httpx
from dacite import from_dict

from interface.AppVersionStrategy import AppVersionStrategy
from lib.apputil import get_final_url
from lib.sysutil import get_system_info
from type.index import AppStoreAppInfo, BrewUrlInfo


class BrewStrategy(AppVersionStrategy):
    def get_version_info(self, link, old_version_info) -> "AppStoreAppInfo":

        response = httpx.get(url=link)
        brew_json = json.loads(response.content)

        brew_url_info = from_dict(data_class=BrewUrlInfo, data=brew_json)

        system_info = get_system_info()

        url_info = None
        if system_info.architecture == 'Intel':
            url_info = get_final_url(brew_url_info.url)

        if system_info.architecture == 'ARM':
            url_info = get_final_url(brew_url_info.variations.arm64_sonoma.url)

        return AppStoreAppInfo(old_version_info.showVersion, brew_url_info.version, url_info.lastModified,
                               url_info.realDownloadUrl,
                               brew_url_info.version != old_version_info.compareVersion)
