from typing import Any


def filler(data: dict[str, Any]):
    """Filler"""
    return {key: value for key, value in data.items() if value is not None}


def discard_when_matched(data: dict[str, Any], against: dict[str, Any]):
    """Discard when matched, i.e when a data is already present"""
    return {key: value for key, value in data.items() if key in against}
