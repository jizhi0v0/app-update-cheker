import json

import httpx
from dacite import from_dict

from interface.AppVersionStrategy import AppVersionStrategy
from lib.apputil import get_final_url
from lib.sysutil import get_system_info
from type.index import AppStoreAppInfo, PostmanUrlInfo


class PostmanStrategy(AppVersionStrategy):
    def get_version_info(self, link, old_version_info) -> "AppStoreAppInfo":

        response = httpx.get(url=link)
        brew_postman_json = json.loads(response.content)

        postman_url_info = from_dict(data_class=PostmanUrlInfo, data=brew_postman_json)

        system_info = get_system_info()

        url_info = None
        if system_info.architecture == 'Intel':
            url_info = get_final_url(postman_url_info.url)

        if system_info.architecture == 'ARM':
            url_info = get_final_url(postman_url_info.variations.arm64_sonoma.url)

        return AppStoreAppInfo(old_version_info.showVersion, postman_url_info.version, url_info.lastModified,
                               url_info.realDownloadUrl,
                               postman_url_info.version != old_version_info.compareVersion)
