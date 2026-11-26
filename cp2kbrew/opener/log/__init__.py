from . import v2022_2, v2025_1


# the v2025.1 parser also reads CP2K 2026.2 logs
log_versions = {"v2022.2": v2022_2, "v2025.1": v2025_1, "v2026.2": v2025_1}


def get_logger(version: str):
    if version not in log_versions:
        raise ValueError(f"Unknown CP2K log version {version!r}; choose one of {sorted(log_versions)}")
    return log_versions[version]
