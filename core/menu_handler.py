from constants import SUPPORTED_FORMATS
from core import MetadataHandler
import os, sys
from pathlib import Path


class MenuHandler:
    def __init__(self, metadata_handler: "MetadataHandler", audios_dir: str):
        self.metadata_handler = metadata_handler
        self.audios_dir = audios_dir
        self.choices = {
            "1": self.process_all_files,
            "2": self.process_single_file,
            "0": self.exit_program
        }

    def show_menu(self):
        while True:
            print("\nSound Library")
            print("1. 오디오 파일 전체 메타데이터")
            print("2. 오디오 파일 단일 메타데이터")
            print("0. 종료")
            choice = input("선택하세요: ")

            if choice in self.choices:
                self.choices[choice]()
            else:
                print("잘못된 선택입니다. 다시 시도해주세요.")

    def process_all_files(self):
        """
        1. 오디오 파일 전체 메타데이터
        :param
        :return:
        """
        audio_files = self.get_audio_files()  # audios_dir을 주지 않아도 한 객체 내에 있기때문에 알아서 변수를 사용할 것이다.
        # if not audio_files:
        #     print("오디오 목록이 없습니다.")
        #     return
        for audio_file in audio_files:
            self.metadata_handler.process_file(audio_file)

    def process_single_file(self):
        """
        2. 오디오 파일 전체 메타데이터
        :return:
        """
        audio_files = self.get_audio_files()
        if not audio_files:
            print("오디오 목록이 없습니다.")
            return

        try:
            file_index = input(f"\n조회할 파일 번호를 선택하세요 (1-{len(audio_files)}): ")
            audio_title = audio_files[int(file_index) - 1]
            audio_dir = str(Path(self.audios_dir, audio_title))

            self.metadata_handler.read_audio_metadata(audio_dir, audio_title)

            if input("메타데이터 관리를 시작하시겠습니까? (yes/no): ").lower() == 'yes':
                self.metadata_handler.crud(audio_dir)
            else:
                print("메타데이터 관리를 취소합니다.")

        except (ValueError, IndexError) as e:
            print(f"오류: 올바른 파일 번호를 입력해주세요. ({e})")
        # 파일 선택 및 처리 로직

    @staticmethod
    def exit_program():
        print("프로그램을 종료합니다.")
        sys.exit(0)

    def get_audio_files(self) -> list:
        """
        오디오 파일 목록 반환 로직
        """
        # audio_list = []
        # for f in os.listdir(self.audios_dir):
        #     if f.lower().endswith(SUPPORTED_FORMATS):
        #         audio_list.append(f)
        # return audio_lis
        audio_files = [f for f in os.listdir(self.audios_dir) if f.lower().endswith(SUPPORTED_FORMATS)]
        if not audio_files:
            print("처리할 오디오 파일이 없습니다.")
            return []

        return audio_files
