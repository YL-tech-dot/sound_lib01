# utils.py
import os


def get_metadata_keys(metadata: dict, keys: str):
    """
    메타데이터 딕셔너리에서 특정 키의 값을 추출 반환.
    """
    return {key: metadata.get(key, "정보 없음") for key in keys}
