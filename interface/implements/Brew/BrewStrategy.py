import json

import httpx
from dacite import from_dict

from interface.AppVersionStrategy import AppVersionStrategy
from lib.apputil import get_final_url, get_version_from_brew_url_info
from lib.sysutil import get_system_info
from type.index import AppStoreAppInfo, BrewUrlInfo


class BrewStrategy(AppVersionStrategy):
    def get_version_info(self, link, old_version_info) -> "AppStoreAppInfo":

        response = httpx.get(url=link)
        brew_json = json.loads(response.content)

        brew_url_info = from_dict(data_class=BrewUrlInfo, data=brew_json)

        url_info = None

        if brew_url_info.variations.arm64_sonoma is None:
            url_info = get_final_url(brew_url_info.url)
        else:
            system_info = get_system_info()

            if system_info.architecture == 'Intel':
                url_info = get_final_url(brew_url_info.url)

            if system_info.architecture == 'ARM':
                url_info = get_final_url(brew_url_info.variations.arm64_sonoma.url)

        real_version = get_version_from_brew_url_info(brew_url_info, old_version_info.appName)
        return AppStoreAppInfo(old_version_info.showVersion, real_version, url_info.lastModified,
                               url_info.realDownloadUrl,
                               real_version != old_version_info.compareVersion)
