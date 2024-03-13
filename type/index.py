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


@dataclass
class Arm64Sonoma:
    url: str


@dataclass
class Variations:
    arm64_sonoma: Arm64Sonoma


@dataclass
class PostmanUrlInfo:
    url: str
    version: str
    variations: Variations


@dataclass
class SystemInfo:
    os_type: str
    architecture: str

