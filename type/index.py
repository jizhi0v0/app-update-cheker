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
    appName: str


@dataclass
class DownloadUrlInfo:
    lastModified: str
    realDownloadUrl: str


@dataclass
class Arm64Sonoma:
    url: str
    version: Optional[str] = None


@dataclass
class Variations:
    arm64_sonoma: Optional[Arm64Sonoma] = None


@dataclass
class BrewUrlInfo:
    url: str
    version: str
    variations: Variations


@dataclass
class SystemInfo:
    os_type: str
    architecture: str

