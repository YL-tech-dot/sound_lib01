import os
import subprocess
import json
# from pathlib import Path
# from pydub.utils import mediainfo # 사운드 파일 로드
# from pydub import AudioSegment

def list_audio_files(directory):
    """
    가나다 or abc 순서대로 나열됩니다.
    python은 유니코드를 기반하므로 한글 정렬도 지원됩니다.
    """
    supported_formats = (".mp3", ".wav", ".flac", ".ogg")
    files = [
        f for f in os.listdir(directory) if f.endswith(supported_formats)
    ]
    files = sorted(files)
    return files

# 1개의 오디오 메타데이터 추출
def get_audio_metadata(file_path):
    """
    :param file_path: 오디오파일 경로 : str
    :return: metadata_dict : dict
    """
    # ffprobe.exe 명령어 실행
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
    # stdout 표준 출력은 pipe를 통해 캡처하도록 지정함
    # stderr 표준 오류를 파이프 다른 프로세스와의 연결을 통해 캡처하도록 지정.
    # python 3.7이상에선 text = True가 필요하여 추가함.

    # JSON 결과 파싱
    metadata_dict = json.loads(result.stdout)
    print(metadata_dict)
    metadata = metadata_dict['streams'][0]
    # print(metadata)
    # 메타데이터 출력
    print(f"길이: {float(metadata['duration']):.2f}초")
    print(f"채널 수: {metadata.get('channels', '정보 없음')}")
    print(f"샘플링 주파수: {metadata.get('sample_rate','정보 없음')}Hz")
    print(f"비트레이트: {metadata.get('bit_rate','정보 없음')}bps")
    print(f"비트 깊이: {metadata.get('bit_depth', '정보 없음')}")
    # codec 관련 키 출력
    codec = next((metadata[key] for key in metadata if 'codec' in key), None)
    print(f"코덱: {codec if codec else '정보 없음'}")

    return metadata

# 메타데이터를 json 파일로 저장하는 함수
def save_metadata_json(metadata, file_name="metadata0.json"):
    """
    메타데이터를 json 파일로 저장하는 함수
    :param metadata: audio file's info : dict
    :param file_name: 메타데이터 저장할 이름 str
    :return: None
    """
    # numb = 0
    if os.path.exists(file_name):
        # file name에 숫자 넣기
        # numb += 1
        # file_name = file_name + f"0{numb}"
        with open(file_name, "r") as f:
            existing_data = json.load(f) # json 파일 내용 ( json -> dict )
            print(existing_data)
            print("파일이 기존에 저장되어있습니다. 새로 덮어쓰시겠습니까?")
    else:
        existing_data = {}
        print("기존에 저장된 데이터가 없습니다. 새로 저장을 시작하시겠습니까?")

    user_answer = input("yes / no\n>>>")

    if user_answer == "yes": # metadata를 추가하고 파일로 저장
        existing_data[file_name] = metadata
        with open(file_name, "w") as save:
            json.dump(existing_data, save, indent=4) # python 객체를 json형식 문자열로 변환해 파일 저장 (dict -> json)
        print("새로 저장되었습니다.")

    elif user_answer == "no":
        print("저장되지 않았습니다.")

    print(f"---\n현재 파일: {existing_data}\n---")

# file_path = r"C:/projects/sound_lib01/sounds/downfall-3-208028.mp3"
# get_audio_metadata(file_path)

def update_metadata_json(metadata, file_name="metadata0.json"):
    """
        메타데이터를 json 파일로 저장하는 함수
        :param metadata: audio file's info : dict
        :param file_name: 메타데이터 저장할 이름 str
        :return: None
        """

    # 읽기 전용
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            existing_data = json.load(f)  # json 파일 내용 ( json -> dict )
            existing_data.readline()
    else:
        existing_data = {}
        print("기존에 저장된 데이터가 없습니다.")

    # metadata를 추가하고 파일로 저장
    existing_data[file_name] = metadata
    with open(file_name, "w") as f:
        json.dump(existing_data, f, indent=4)  # python 객체를 json형식 문자열로 변환해 파일 저장 (dict -> json)

    print("\nexisting_data : ")
    print(existing_data)
    print()

def del_metadata_json(metadata, file_name="metadata0.json"):
    """
            메타데이터를 json 파일로 저장하는 함수
            :param metadata: audio file's info : dict
            :param file_name: 메타데이터 저장할 이름 str
            :return: None
            """
    try:
        # 읽기 전용
        user_answer = input("삭제하려는 것은 메타데이터의 항목이라면 key, 파일 이름이라면 file을 입력해주세요.\n>>>")

        if user_answer =="file":
            if os.path.exists(file_name):
                with open(file_name, "r") as f:
                    existing_data = json.load(f)  # json 파일 내용 ( json -> dict )
                    existing_data.readline()
                # existing data를 삭제하는 코드 구현
            else:
                print(f"{file_name}이 없습니다.")

        elif user_answer == "key":
            key = input("어떤 항목인지 입력해주세요")
            if os.path.exists(file_name):
                with open(file_name, "r") as f:
                    existing_data = json.load(f)  # json 파일 내용 ( json -> dict )
                    existing_data.readline()
                # existing data를 삭제하는 코드 구현
                    if key in existing_data[key]:
                        del existing_data[key]
                        json.dump()
            else:
                print("해당 항목은 없습니다.")
        else:
            print("기존에 저장된 데이터가 없습니다.")
    except (ValueError, IndexError) as e:
        print(f"error>>>{e}")

