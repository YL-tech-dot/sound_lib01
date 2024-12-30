# main.py 진입점
from pathlib import Path
import os
import subprocess
import sys
from core import MenuHandler, MetadataHandler


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


def main():
    print("안녕하세요 오디오 라이브러리 관리 프로그램입니다.\nffpobe 설치여부를 확인하겠습니다.\n")
    check = check_ffprobe()
    if not check:
        print("프로그램을 종료합니다.")
        return sys.exit(1)

    audios_dir = get_directory_input()
    menu = MenuHandler(MetadataHandler(audios_dir),audios_dir=audios_dir)
    # 사용자가 탐색할 오디오 경로
    print("오디오 탐색을 시작하겠습니다.")
    # menu 탐색할 오디오 시작
    menu.show_menu()


if __name__ == "__main__":
    main()
