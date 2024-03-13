import httpx
from lxml import etree

from interface.AppVersionStrategy import AppVersionStrategy
from type.index import AppStoreAppInfo


class AppStoreStrategy(AppVersionStrategy):
    def get_version_info(self, link, old_version_info) -> "AppStoreAppInfo":
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/"
                          "122.0.0.0 Safari/537.36"
        }
        response = httpx.get(link, headers=headers)
        tree = etree.HTML(response.content)

        version_tag = tree.xpath('//p[contains(@class, "whats-new__latest__version")]')[0]
        previous_sibling = version_tag.xpath('preceding-sibling::*[1]')

        release_date = 'Unknown'
        if previous_sibling:
            release_date: str = previous_sibling[0].text
        else:
            print("No previous element found.")

        latest_version: str = version_tag.text.replace('Version ', '')
        return AppStoreAppInfo(
            oldVersion=old_version_info.showVersion,
            latestVersion=latest_version,
            releaseDate=release_date,
            downloadUrl=link,
            needUpdate=(old_version_info.compareVersion != latest_version)
        )

