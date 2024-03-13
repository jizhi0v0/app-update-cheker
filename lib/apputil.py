import os
import plistlib
from lxml import etree
import httpx
from type.index import AppStoreAppInfo, DownloadUrlInfo

plist = 'Info.plist'


def read_info_plist(file_path, plist_name):
    plist_into_path = os.path.join(file_path, plist_name)
    if os.path.exists(plist_into_path):
        with open(plist_into_path, 'rb') as file:
            return plistlib.load(file)
    else:
        return None


def get_final_url(url: str) -> DownloadUrlInfo:
    with httpx.Client() as client:
        with client.stream(method="GET", url=url, follow_redirects=True) as response:
            final_url = str(response.url)
            last_modified = response.headers.get('Last-Modified', 'Unknown')
            return DownloadUrlInfo(lastModified=last_modified, realDownloadUrl=final_url)


