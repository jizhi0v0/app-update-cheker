import os
import plistlib
import httpx
from type.index import DownloadUrlInfo, BrewUrlInfo

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
            if response.status_code == 200:
                final_url = str(response.url)
                last_modified = response.headers.get('Last-Modified', 'Unknown')
                return DownloadUrlInfo(lastModified=last_modified, realDownloadUrl=final_url)


def transform_string(input_str: str) -> str:
    transformed = input_str.replace(' ', '-')
    transformed = transformed.lower()
    return transformed


def generate_url(input_str):
    base_url = "https://formulae.brew.sh/api/cask/"
    transformed_str = transform_string(input_str)
    final_url = f"{base_url}{transformed_str}.json"
    return final_url


def get_version_from_brew_url_info(data: BrewUrlInfo, app_name: str) -> str:
    # customized logic
    if 'bartender' in app_name.lower():
        return data.variations.arm64_sonoma.version
    return data.version

# print(get_final_url("https://formulae.brew.sh/api/cask/google-chrome.json1"))
