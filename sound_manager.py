# sound_manager.py
import os
import subprocess
import json
from select_interface import get_and_print_metadata, pretty_print_dict  # 메타데이터 출력 함수


def get_audio_metadata(file_path: str):
    """
    1개의 오디오 메타데이터 추출
    ffprobe.exe 를 cmd에서 명령어와 함께 실행시켜 선택된 오디오의 메타정보를 얻는다.
    :param file_path: 오디오파일 경로 : str
    :return: metadata_dict : dict
    stdout 표준 출력은 pipe를 통해 캡처하도록 지정함
    stderr 표준 오류를 파이프 다른 프로세스와의 연결을 통해 캡처하도록 지정.
    python 3.7이상에선 text = True가 필요하여 추가함.
    """
    cmd = [
        "ffprobe",  # cmd 창에서 ffprobe 실행
        "-v", "error",  # 로그 수준 설정, "error"로 설정하여 에러만 출력
        "-show_streams",
        # "-select_streams", "a:0",  # 첫 번째 오디오 스트림 선택 (a:0은 첫 번쨰 오디오 스트림을 의미)
        # "-show_entries", "stream=duration,channels,sample_rate,bit_rate",
        "-of", "json",  # JSON 형식으로 출력
        file_path  # 오디오 파일 경로 (파일 경로는 변수로 제공)
    ]
    # ffprobe.exe 명령어 실행 후 결과 받기
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # JSON 결과 파싱
    metadata_dict = json.loads(result.stdout)
    metadata = metadata_dict['streams'][0]

    # 메타데이터 출력
    get_and_print_metadata(metadata)

    return metadata


# 메타데이터를 json 파일로 저장하는 함수
def save_metadata_json(metadata: dict, file_name="metadata0.json"):
    """
    메타데이터를 json 파일로 저장하는 함수
    :param metadata: audio file's info
    :param file_name: 메타데이터 저장할 이름
    :return: None
    """
    # numb = 0
    if os.path.exists(file_name):
        # file name에 숫자 넣기
        # numb += 1
        # file_name = file_name + f"0{numb}"
        with open(file_name, "r") as f:
            existing_data = json.load(f)  # json 파일 내용 ( json -> dict )
        print("파일이 기존에 저장되어있습니다. 새로 덮어쓰시겠습니까?")
    else:
        existing_data = {}
        print("기존에 저장된 데이터가 없습니다. 새로 저장을 시작하시겠습니까?")

    user_answer = input("yes / no\n>>>")

    if user_answer == "yes":  # metadata를 추가하고 파일로 저장
        existing_data[file_name] = metadata
        with open(file_name, "w") as save:
            json.dump(existing_data, save, indent=4)  # python 객체를 json형식 문자열로 변환해 파일 저장 (dict -> json)
        print("새로 저장되었습니다.")
        print(f"{pretty_print_dict(existing_data)}")
    elif user_answer == "no":
        print("저장되지 않았습니다.")

    print(f"---\n현재 파일: {existing_data}\n---")


def update_metadata_json(file_path):
    """
        메타데이터를 json 파일로 저장하는 함수
        :param metadata: audio file's info
        :param file_name: 메타데이터 저장할 이름
        :return: None
        """
    # 읽기 전용
    metadata = get_audio_metadata(file_path)
    if metadata:
        pretty_print_dict(metadata)  # 수정항 목 view
        key_to_update = input("수정할 key를 입력: ")
        new_value = input(f"{key_to_update}의 새로운 값을 입력하세요: ")

        if key_to_update in metadata:
            metadata[key_to_update] = new_value
            update_metadata_json(metadata)
            print(f"{key_to_update}가 {new_value}로 수정되었습니다.")
        else:
            print("해당 key가 존재하지 않습니다.")
    else:
        print("메타데이터를 찾을 수 없습니다.")


def del_metadata_json(file_path):
    """
    JSON 파일에서 특정 메타데이터 항목 또는 파일 이름 전체 삭제
    :param delete_file: 삭제할 파일 이름(전체 데이터 삭제)
    :param delete_key: 삭제할 메타데이터의 특정 필드 (예: 'duration')
    :param file_name: 메타데이터가 저장된 JSON 파일 이름
    :return: None
    """
    metadata = get_audio_metadata(file_path)
    if metadata:
        pretty_print_dict(metadata)  # 삭제할 항목을 보기 좋게 출력
        del_choice = input("삭제할 항목을 선택하세요. (key / field): ")

        if del_choice == "key":
            key_to_delete = input("삭제할 key를 입력하세요: ")
            if key_to_delete in metadata:
                del metadata[key_to_delete]
                del_metadata_json(metadata)
                print(f"{key_to_delete}가 삭제되었습니다.")
            else:
                print("해당 key가 존재하지 않습니다.")

        elif del_choice == "field":
            field_to_delete = input("삭제할 필드를 입력하세요: ")
            if field_to_delete in metadata:
                del metadata[field_to_delete]
                del_metadata_json(metadata)
                print(f"{field_to_delete}가 삭제되었습니다.")
            else:
                print("해당 필드가 존재하지 않습니다.")

        else:
            print("잘못된 선택입니다.")
    else:
        print("메타데이터를 찾을 수 없습니다.")


# 테스트용
# del_metadata_json(delete_key="codec_name", file_name="metadata0.json")

def metadata_management(file_path):
    print("\n\n메타데이터 관리")
    metadata_action = input("저장(save) / 수정(update) / 삭제(del): ")

    if metadata_action == "save":
        save_metadata_json(file_path)
    elif metadata_action == "update":
        update_metadata_json(file_path)
    elif metadata_action == "del":
        del_metadata_json(file_path)
    else:
        print("잘못된 선택입니다. 다시 선택해주세요.")
