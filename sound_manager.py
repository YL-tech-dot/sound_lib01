import os
import subprocess
import json
from pathlib import Path
# from pydub.utils import mediainfo # 사운드 파일 로드
from pydub import AudioSegment

def process_directory(directory, output_file="metadata.json"):
    # 파일 탐색
    supported_formats = (".mp3", ".wav", ".flac", ".ogg")
    files = [
        f for f in os.listdir(directory) if f.endswith(supported_formats)
    ]
    files = sorted(files)
    cmd = [
        "ffprobe",  # cmd 창에서 ffprobe 실행
        "-v", "error",  # 로그 수준 설정, "error"로 설정하여 에러만 출력
        # "-show_streams",
        "-select_streams", "a:0",  # 첫 번째 오디오 스트림 선택 (a:0은 첫 번쨰 오디오 스트림을 의미)
        "-show_entries", "stream=duration,channels,sample_rate,bit_rate",
        # 추출할 항목 지정:duration,channels,sample_rate,bitrate
        "-of", "json",  # JSON 형식으로 출력
        directory  # 오디오 파일 경로 (파일 경로는 변수로 제공)
    ]

    # ffprobe 명령어 실행 후 결과 받기
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # stdout 표준 출력은 pipe를 통해 캡처하도록 지정함
    # stderr 표준 오류를 파이프 다른 프로세스와의 연결을 통해 캡처하도록 지정.
    # python 3.7이상에선 text = True가 필요함.

    # JSON 결과 파싱
    metadata = json.loads(result.stdout)

    # 오디오 정보 출력
    duration = metadata['streams'][0]['duration']
    channels = metadata['streams'][0]['channels']
    sample_rate = metadata['streams'][0]['sample_rate']
    bit_rate = metadata['streams'][0]['bit_rate']

    print(f"파일: {directory}")
    print(f"길이: {float(duration):.2f}초")
    print(f"채널 수: {channels}")
    print(f"샘플링 주파수: {sample_rate}Hz")
    print(f"비트레이트: {bit_rate}bps")
    # 메타데이터 추출
    # JSON 저장

def list_audio_files(directory):
    supported_formats = (".mp3", ".wav", ".flac", ".ogg")
    files = [
        f for f in os.listdir(directory) if f.endswith(supported_formats)
    ]
    files = sorted(files)
    """
    가나다 or abc 순서대로 나열됩니다. 
    python은 유니코드를 기반하므로 한글 정렬도 지원됩니다.
    """
    return files

# 1개의 오디오 메타데이터 추출
def get_audio_metadata(file_path):
    """
    :param file_path: 오디오파일 경로 : str
    :return: metadata_dict : dict
    """
    # ffprobe 명령어 실행
    cmd = [
        "ffprobe",  # cmd 창에서 ffprobe 실행
        "-v", "error",  # 로그 수준 설정, "error"로 설정하여 에러만 출력
        # "-show_streams",
        "-select_streams", "a:0",  # 첫 번째 오디오 스트림 선택 (a:0은 첫 번쨰 오디오 스트림을 의미)
        "-show_entries", "stream=duration,channels,sample_rate,bit_rate",
        # 추출할 항목 지정:duration,channels,sample_rate,bitrate
        "-of", "json",  # JSON 형식으로 출력
        file_path  # 오디오 파일 경로 (파일 경로는 변수로 제공)
    ]

    # ffprobe 명령어 실행 후 결과 받기
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # stdout 표준 출력은 pipe를 통해 캡처하도록 지정함
    # stderr 표준 오류를 파이프 다른 프로세스와의 연결을 통해 캡처하도록 지정.
    # python 3.7이상에선 text = True가 필요함.

    # JSON 결과 파싱
    metadata_dict = json.loads(result.stdout)

    # 오디오 정보 출력
    duration = metadata_dict['streams'][0]['duration']
    channels = metadata_dict['streams'][0]['channels']
    sample_rate = metadata_dict['streams'][0]['sample_rate']
    bit_rate = metadata_dict['streams'][0]['bit_rate']

    # 결과 안내
    print(f"파일: {file_path}")
    print(f"길이: {float(duration):.2f}초")
    print(f"채널 수: {channels}")
    print(f"샘플링 주파수: {sample_rate}Hz")
    print(f"비트레이트: {bit_rate}bps")

    return metadata_dict


# file_path = r"C:/projects/sound_lib01/sounds/downfall-3-208028.mp3"
# get_audio_metadata(file_path)

# 메타데이터를 json 파일로 저장하는 함수
def save_metadata_json(metadata, file_name="metadata.json"):
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

    else:
        existing_data = {}
        print("existing_data가 없습니다.")

    # metadata를 추가하고 파일로 저장
    existing_data[file_name] = metadata
    with open(file_name, "w") as f:
        json.dump(existing_data, f, indent=4) # python 객체를 json형식 문자열로 변환해 파일 저장 (dict -> json)

    print("\nexisting_data : ")
    print(existing_data)
    print()

# file_path = r"C:/projects/sound_lib01/sounds/downfall-3-208028.mp3"
# get_audio_metadata(file_path)



