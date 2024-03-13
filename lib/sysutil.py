import platform

from type.index import SystemInfo


def get_system_info() -> SystemInfo:
    os_name = platform.system()
    architecture = platform.machine()

    if os_name == "Darwin":
        os_type = "macOS"
    elif os_name == "Windows":
        os_type = "Windows"
    elif os_name == "Linux":
        os_type = "Linux"
    else:
        os_type = "Unknown OS"

    # 特别地，macOS可能运行在Intel或ARM架构上
    if os_type == "macOS" and architecture == "arm64":
        arch_info = "ARM"
    elif os_type == "macOS" and architecture.startswith("x86"):
        arch_info = "Intel"
    else:
        arch_info = architecture

    return SystemInfo(os_type, arch_info)


get_system_info()
