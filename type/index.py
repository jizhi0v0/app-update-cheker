from dataclasses import dataclass
from typing import Optional


@dataclass
class AppStoreAppInfo:
    # OldVersionInfo.showVersion
    oldVersion: str
    latestVersion: str
    releaseDate: Optional[str]
    downloadUrl: str
    needUpdate: bool


@dataclass
class OldVersionInfo:
    # for react.js
    showVersion: str
    compareVersion: str


@dataclass
class DownloadUrlInfo:
    lastModified: str
    realDownloadUrl: str
