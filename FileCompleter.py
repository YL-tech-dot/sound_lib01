from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import os


class FileCompleter(Completer):
    def __init__(self, directory):
        self.directory = directory

    def get_completions(self, document, complete_event):
        # 입력된 부분에 맞는 파일 및 디렉토리 목록을 반환
        for filename in os.listdir(self.directory):
            if filename.startswith(document.text):  # 입력된 텍스트와 일치하는 항목만 필터링
                yield Completion(filename, start_position=-len(document.text))


def get_file_input(directory):
    completer = FileCompleter(directory)

    # 입력받을 때 자동 완성을 지원하는 프롬프트
    try:
        file_input = prompt('파일 경로: ', completer=completer)
    except Exception as e:
        print(f"오류 발생: {e}")
        file_input = None

    return file_input


# 사용 예시
directory = 'C:/path/to/your/directory'  # 자동 완성을 원하는 디렉토리
file_path = get_file_input(directory)
if file_path:
    print(f"선택된 파일: {file_path}")
else:
    print("파일 입력이 취소되었습니다.")
