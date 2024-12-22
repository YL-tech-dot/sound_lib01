# select_interface.py
# 출력, 선택
from utils import list_audio_files, get_metadata_keys # utils에서 가져옴

def get_and_print_audio_files(directory: str):
    """
    디렉토리에서 오디오 파일 목록을 출력하고 반환
    """
    audio_files = list_audio_files(directory)
    if not audio_files:
        print("\n탐색된 파일이 없습니다.")
        return []

    print("\n오디오 파일: ")
    for i, audio_file in enumerate(audio_files, start=1):
        print(f"{i}. {audio_file}") # 결과: [(1, "sound1.mp3"), (2, "sound2.wav")]

    return audio_files

def get_and_print_metadata(metadata: dict):
    """
        디렉토리에서 오디오 파일 목록을 출력하고 반환
    """
    if not metadata:
        print("메타 데이터가 없습니다.")
        return

    print("-" * 10)
    print(f"길이: {float(metadata['duration']):.2f}초")
    print(f"채널 수: {metadata.get('channels', '정보 없음')}")
    print(f"샘플링 주파수: {metadata.get('sample_rate', '정보 없음')}Hz")
    print(f"비트레이트: {metadata.get('bit_rate', '정보 없음')}bps")
    print(f"비트 깊이: {metadata.get('bit_depth', '정보 없음')}")
    # codec 관련 키 출력
    codec = next((metadata[key] for key in metadata if 'codec' in key), None)
    print(f"코덱: {codec if codec else '정보 없음'}")
    print("-" * 10)

def pretty_print_dict(data: dict, indent: int=0):
    """
    오디오 메타데이터 출력
        1. 가독성: 딕셔너리의 계층 구조를 들여쓰기를 통해 명확히 표현
        2. 재귀 호출: 중첩된 딕셔너리도 동일한 방식으로 출력
        3. 유연성: 들여쓰기 수준(indent)을 조정하여 출력 형식 custom
    :param data:
    :param indent:
    :return: None

    ex:
    'address:
        city: Seoul
        zipcode: 12345'
    """
    print("-"*10)
    for key, value in data.items(): # data.items() = data 딕셔너리의 key-value 쌍
        print(" " * indent + f"{key}: ", end="")
        if isinstance(value, dict): # isinstance = 값이 딕셔너리인지 확인하는 메서드
            print()  # 줄바꿈
            pretty_print_dict(value, indent=indent + 4)  # 재귀 호출로 하위 딕셔너리 출력

        else:
            print(value) # 줄바꿈 포함.
    print("-"*10)