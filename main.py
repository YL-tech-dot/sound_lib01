# main.py
from pathlib import Path
import module.interface as inter
import module.metadata as meta
import os
import subprocess
import sys
from module.metadata import Metadata


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


def process_single_audio(audio_meta:'Metadata', audio_files:list):
    try:
        file_index = input(f"\n조회할 파일 번호를 선택하세요 (1-{len(audio_files)}): ")
        audio_title = audio_files[int(file_index) - 1]
        audio_directory = str(Path(audio_meta.audios_directory, audio_title))

        audio_meta.read_audio_metadata(audio_directory, audio_title)

        if input("메타데이터 관리를 시작하시겠습니까? (yes/no): ").lower() == 'yes':
            audio_meta.crud(audio_directory)
        else:
            print("메타데이터 관리를 취소합니다.")

    except (ValueError, IndexError) as e:
        print(f"오류: 올바른 파일 번호를 입력해주세요. ({e})")

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
    print("ffpobe 설치여부 확인이 완료되었습니다.\n")
    # 사용자가 탐색할 오디오 경로
    print("오디오 탐색을 시작하겠습니다.")
    audios_directory = str(get_directory_input())
    audio_meta = meta.Metadata(audios_directory)
    print("탐색할 오디오 경로가 확인되었습니다.\n")

    while True:
        print("\n\nSound Library")
        print("1. 오디오 파일 전체 : 메타데이터 ")
        print("2. 오디오 파일  1개 : 메타데이터 ")
        print("0. 종료")
        choice = input("선택하세요:")

        # 1. 사운드 파일 탐색
        if choice == "1":
            audio_files = inter.get_audio_list(audios_directory)
            if not audio_files:
                continue  # 반복문으로 돌아감

            print("\n===Start===")
            for audio_title in audio_files:
                file_path = str(Path(audios_directory, audio_title))  # type을 명시적으로 str로 캐스팅
                print("filepath_:", file_path)
                audio_meta.read_audio_metadata(file_path, audio_title)
            print("===End===\n")

        # 2. Audio file 목록 출력
        elif choice == "2":
            audio_files = inter.get_audio_list(audios_directory)
            process_single_audio(audio_meta, audio_files)

        elif choice == "0":
            print("종료합니다.")
            break

        else:

            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
