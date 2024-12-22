# utils.py
import os

def list_audio_files(directory: str):
    """
    지정된 디렉토리에서 오디오 파일 목록을 반환합니다.
    """
    supported_formats = (".mp3", ".wav", ".flac", ".ogg")
    files = [f for f in os.listdir(directory) if f.endswith(supported_formats)]
    return sorted(files)  # 가나다 또는 abc 순서대로 정렬


def get_metadata_keys(metadata: dict, keys: str):
    """
    메타데이터 딕셔너리에서 특정 키의 값을 추출 반환.
    """
    return {key: metadata.get(key, "정보 없음") for key in keys}