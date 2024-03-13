from abc import ABC, abstractmethod

from type.index import AppStoreAppInfo, OldVersionInfo


class AppVersionStrategy(ABC):
    @abstractmethod
    def get_version_info(self, link: str, old_version_info: OldVersionInfo) -> "AppStoreAppInfo":
        pass


def get_app_info(link: str, old_version_info: OldVersionInfo, strategy: AppVersionStrategy) -> "AppStoreAppInfo":
    return strategy.get_version_info(link, old_version_info)
