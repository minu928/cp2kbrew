from . import v2022_2, v2025_1


log_versions = {"v2022.2": v2022_2, "v2025.1": v2025_1}


def get_logger(version: str):
    return log_versions.get(version, None)
