from utils import list_audio_files
from sound_manager import get_audio_metadata, save_metadata_json, update_metadata_json, del_metadata_json
from select_interface import get_and_print_audio_files, pretty_print_dict, metadata_management
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import PathCompleter
import os


# FileCompleter 클래스 정의
class FileCompleter(Completer):
    def __init__(self, directory):
        self.directory = directory

    def get_completions(self, document, complete_event):
        # 입력된 부분에 맞는 파일 및 디렉토리 목록을 반환
        for filename in os.listdir(self.directory):
            if filename.startswith(document.text):  # 입력된 텍스트와 일치하는 항목만 필터링
                yield Completion(filename, start_position=-len(document.text))


# 경로를 입력받는 함수
def get_directory_input(default_directory):
    # PathCompleter를 사용하여 자동 완성 기능을 제공
    completer = PathCompleter(expanduser=True)

    # 기본 디렉토리 경로 설정
    session = PromptSession(completer=completer)

    # 기본 경로를 제공하여 입력받기
    directory_input = session.prompt(f"오디오 파일 경로를 입력하세요: [{default_directory}] ", default=default_directory)
    directory_input = directory_input.replace("/", "\\").replace("\\\\", "\\")  # '\'을 '\\'로 처리
    return directory_input


def main():
    # 1. 디렉토리 경로 입력받기

    while True:
        print("\n\nSound Library")
        print("1. 오디오 파일 전체 탐색")
        print("2. 오디오 파일 1개 메타데이터 보기")
        print("3. 오디오 파일 1개 메타데이터 관리")
        print("0. 종료")
        choice = input("선택하세요:")

        # 1. 사운드 파일 탐색
        if choice == "1":
            directory = get_directory_input("C:\\projects\\sound_lib01\\sounds")  # 자동 완성된 경로 입력
            audio_files = get_and_print_audio_files(directory)
            if not audio_files:
                continue  # 반복문으로 돌아감

            for audio_file in audio_files:
                file_path = os.path.join(directory, audio_file)
                get_audio_metadata(file_path)

        # 2. Audio file 목록 출력
        elif choice == "2":
            directory = get_directory_input("C:\\projects\\sound_lib01\\sounds")
            audio_files = get_and_print_audio_files(directory)
            file_index = input("\n조회할 파일 번호를 선택하세요: ")

            try:
                selected_file = audio_files[int(file_index) - 1]
                file_path = os.path.join(directory, selected_file)
                get_audio_metadata(file_path)

            except (ValueError, IndexError) as e:  # ValueError나 IndexError가 발생했을 때만 처리
                print(f"Error: {e}")

        # 3. Audio file 목록 출력
        elif choice == "3":
            print("메타데이터 관리")
            directory = get_directory_input("C:\\projects\\sound_lib01\\sounds")
            audio_files = list_audio_files(directory)

            if audio_files:
                print("\n오디오 파일: ")
                for i, audio_file in enumerate(audio_files, start=1):
                    print(f"{i}. {audio_file}")
                file_index = input("관리할 파일 번호를 선택하세요: ")

                try:
                    selected_file = audio_files[int(file_index) - 1]
                    print(f"\n선택한 파일: {selected_file}")

                    file_path = os.path.join(directory, selected_file)
                    metadata_management(file_path)

                except (ValueError, IndexError) as e:
                    print(f"Error: {e}")
            else:
                print("\n탐색된 파일이 없습니다.")

        elif choice == "0":
            print("종료합니다.")
            break

        else:

            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
