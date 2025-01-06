# file_utils.py
# 파일 경로 검증과 오디오 파일 확인 등의 유틸리티 함수들을 분리
import os
import subprocess
from pathlib import Path
from constants import SUPPORTED_FORMATS # 전역변수도 import로 불러올 수가 있다.

# 경로를 입력받는 함수
def get_directory_input():
    directory_input = input("탐색할 오디오 파일 경로를 입력하세요: ").strip()

    # 입력값이 비어있는 경우 early return
    if not directory_input:
        print("경로가 입력되지 않았습니다.")
        return None

    audios_directory = str(Path(directory_input).resolve())

    # 경로가 존재하지 않는 경우 early return
    if not os.path.exists(audios_directory):
        print(f"오류: 경로 '{audios_directory}'가 존재하지 않습니다.")
        return None

    # 경로가 디렉토리가 아닌 경우 early return
    if not os.path.isdir(audios_directory):
        print(f"오류: '{audios_directory}'는 디렉토리가 아닙니다.")
        return None

    print(f"탐색할 오디오 경로: {audios_directory}")
    return audios_directory

# ffprobe 설치여부 판별기
def check_ffprobe() -> bool:
    try:
        # ffprobe -version 명령어 실행
        result = subprocess.run(['ffprobe', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("ffprobe가 설치되어 있습니다.\n")
            print(f"버전 정보:\n{result.stdout}\n\n")
            return True
        else:
            print(f"\n\nffprobe 실행 중 오류 발생\n오류 메시지: {result.stderr}")
            return False

    except FileNotFoundError:
        print("ffprobe가 설치되어 있지 않습니다. 다시 설치해주세요.")
        return False

def validate_path(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)

def is_audio_file(filename: str) -> bool:
    return filename.lower().endswith(SUPPORTED_FORMATS)

def get_audio_list(directory: str) -> list[str]:
    """
    지정된 디렉토리에서 지원되는 오디오 파일 목록을 검색하고 반환합니다.
    :param
        directory (str): 검색할 디렉토리 경로
    :return
        list[str]: 발견된 오디오 파일명 리스트. 파일이 없으면 빈 리스트 반환
    supported formats:
        .mp3, .wav, .flac, .ogg
    """
    audio_files = [f for f in os.listdir(directory) if f.endswith(SUPPORTED_FORMATS)]  # 지원 가능 형식만

    # 오디오 목록이 없는 경우
    if not audio_files:
        print("\n탐색된 파일이 없습니다.")
        return []

    # 오디오 목록이 있는 경우
    print("\n오디오 파일 목록:")
    for i, audio_file in enumerate(audio_files, start=1):
        print(f"{i}. {audio_file}")

    return audio_files

# 경로를 입력받는 함수
def get_directory_input():
    directory_input = input("탐색할 오디오 파일 경로를 입력하세요: ").strip()

    # 입력값이 비어있는 경우 early return
    if not directory_input:
        print("경로가 입력되지 않았습니다.")
        return None

    audios_directory = str(Path(directory_input).resolve())

    # 경로가 존재하지 않는 경우 early return
    if not os.path.exists(audios_directory):
        print(f"오류: 경로 '{audios_directory}'가 존재하지 않습니다.")
        return None

    # 경로가 디렉토리가 아닌 경우 early return
    if not os.path.isdir(audios_directory):
        print(f"오류: '{audios_directory}'는 디렉토리가 아닙니다.")
        return None

    print(f"탐색할 오디오 경로: {audios_directory}")
    return audios_directory