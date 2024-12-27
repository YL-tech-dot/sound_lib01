# sound_manager.py
import os
import subprocess
import json
from select_interface import get_and_print_metadata, pretty_print_dict  # 메타데이터 출력 함수


def get_audio_metadata(file_path: str | bytes, audio_title: str) -> dict:
    """
    1개의 오디오 메타데이터 추출
    :param file_path: 오디오파일 경로 : str
    :return: metadata_dict : dict
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

    # ffprobe 명령이 실패할 경우 subprocess.run의 result.stderr에 에러 메시지
    if result.returncode != 0:
        print(f"ffprobe 실행 실패: 파일 경로가 잘못되었거나 지원되지 않는 형식일 수 있습니다.\n{result.stderr}")
        return {}

    # JSON 결과 파싱
    try:
        metadata_dict = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("ffprobe 출력 데이터를 JSON으로 변환하는 데 실패했습니다.")
        return {}

    streams = metadata_dict.get("streams")
    if not streams:
        print("스트림 정보가 없습니다. 오디오 파일인지 확인하세요.")
        return {}

    metadata = streams[0]
    get_and_print_metadata(metadata, audio_title)

    return metadata


# 메타데이터를 json 파일로 저장하는 함수
def create_metadata_json(metadata: dict, json_file_path: str) -> None:
    """
    메타데이터를 json 파일로 저장하는 함수
    :param metadata: audio file's info
    :param json_file_path: 메타데이터 저장할 이름
    :return: None
    """
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            existing_data = json.load(f)  # json 파일 내용 ( json -> dict )
        print("파일이 기존에 저장되어있습니다. 새로 덮어쓰시겠습니까?")
    else:
        existing_data = {}
        print("기존에 저장된 데이터가 없습니다. 새로 저장을 시작하시겠습니까?")

    user_answer = input("덮어쓰기 = yes / no\n>>>").strip().lower()

    if user_answer == "yes":  # metadata를 추가하고 파일로 저장
        existing_data[json_file_path] = metadata
        with open(json_file_path, "w") as save:
            json.dump(existing_data, save, indent=4)  # python 객체를 json형식 문자열로 변환해 파일 저장 (dict -> json)
        print("새로 저장되었습니다.")
        print(f"{pretty_print_dict(existing_data)}")

    elif user_answer == "no":
        print("저장되지 않았습니다.")


def update_metadata_json(json_file_path: str) -> None:
    """
    메타데이터를 JSON 파일로 수정하는 함수
    :param json_file_path: 메타데이터가 저장된 JSON 파일 경로
    :return: None
    """
    metadata = get_audio_metadata(json_file_path, json_file_path)

    if not metadata:
        print("메타데이터를 찾을 수 없습니다.")
        return

    if not isinstance(metadata, dict):
        print("메타데이터가 올바른 형식이 아닙니다.")
        return

    if not os.path.exists(json_file_path):
        print(f"{json_file_path} 파일이 존재하지 않습니다.")
        return

    with open(json_file_path, "r") as f:
        metadata = json.load(f)

    # 메타데이터 출력 및 수정 시작
    pretty_print_dict(metadata)
    key_to_update = input("수정할 key를 입력하세요: ").strip()

    if key_to_update not in metadata:
        print(f"'{key_to_update}' 키가 존재하지 않습니다.")
        return

    new_value = input(f"'{key_to_update}'의 새로운 값을 입력하세요: ").strip()
    metadata[key_to_update] = new_value

    # 수정된 메타데이터 저장
    try:
        with open(json_file_path, "w") as f:
            json.dump(metadata, f, indent=4)
        print(f"'{key_to_update}' 키가 '{new_value}'로 수정되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")


# metadata를 삭제하느냐, json 파일을 삭제하느냐?
def delete_metadata_json(json_file_path: str) -> None:
    """
    JSON 파일에서 특정 메타데이터 항목 또는 파일 이름 전체 삭제
    :param json_file_path: 메타데이터가 저장된 JSON 파일 이름
    :return: None
    """
    with open(json_file_path, "r") as f:
        metadata = json.load(f)
    # 삭제할 데이터 출력
    pretty_print_dict(metadata)

    delete_key = input("삭제할 key를 입력하세요: ").strip()
    if delete_key in metadata:
        del metadata[delete_key]
        with open(json_file_path, "d") as f:
            json.dump(metadata, f, indent=4)
        print(f"{delete_key}가 삭제되었습니다.")
    else:
        print("해당 key가 존재하지 않습니다.")


def metadata_management(file_path: str) -> None:
    print("\n\n메타데이터 관리")
    metadata_action = input("저장(save) / 수정(update) / 삭제(del): ")

    # 사용자에게 파일 경로를 입력받아 json 파일을 처리
    json_file_path = f"{input('메타데이터 저장 또는 수정할 JSON 파일 경로를 입력하세요: ').strip()}.json"

    if metadata_action == "save":
        metadata = get_audio_metadata(file_path, json_file_path)
        create_metadata_json(metadata, json_file_path)
    elif metadata_action == "update":
        json_file_path = file_path
        update_metadata_json(json_file_path)
    elif metadata_action == "del":
        json_file_path = file_path
        delete_metadata_json(json_file_path)
    else:
        print("잘못된 선택입니다. 다시 선택해주세요.")
