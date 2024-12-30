# interface.py
import os


def get_audio_list(directory: str) -> list[str]:
    """
    지정된 디렉토리에서 지원되는 오디오 파일 목록을 검색하고 반환합니다.
    :param
        directory (str): 검색할 디렉토리 경로
    :return
        list[str]: 발견된 오디오 파일명 리스트. 파일이 없으면 빈 리스트 반환
    supported formats:
        .mp3, .wav, .flac, .ogg
    """
    supported_formats = (".mp3", ".wav", ".flac", ".ogg")
    audio_files = [f for f in os.listdir(directory) if f.endswith(supported_formats)]  # 지원 가능 형식만

    # 오디오 목록이 없는 경우
    if not audio_files:
        print("\n탐색된 파일이 없습니다.")
        return []

    # 오디오 목록이 있는 경우
    print("\n오디오 파일 목록:")
    for i, audio_file in enumerate(audio_files, start=1):
        print(f"{i}. {audio_file}")

    return audio_files


def print_metadata(metadata: dict, audio_title: str = "None") -> None:
    """
    오디오의 정제된 메타데이터와 오디오 제목을 출력
    :param
        metadata(dict): 출력할 오디오 메타데이터
        audio_title(str): 출력할 오디오 명
    :return
        None
    """
    # 1. 메타 데이터가 없을 경우
    if not metadata:
        print("메타 데이터가 없습니다.")
        return

    # 2. 메타 데이터가 있을 경우 출력
    print("-" * 15)
    print(f"오디오명 : {audio_title}")
    print(f"길이: {float(metadata['duration']):.2f}초")
    print(f"채널 수: {metadata.get('channels', '정보 없음')}")
    print(f"샘플링 주파수: {metadata.get('sample_rate', '정보 없음')}Hz")
    print(f"비트레이트: {metadata.get('bit_rate', '정보 없음')}bps")
    print(f"비트 깊이: {metadata.get('bit_depth', '정보 없음')}")
    codec = next((metadata[key] for key in metadata if 'codec' in key), None)  # codec 관련 키 출력
    print(f"코덱: {codec if codec else '정보 없음'}")


def print_clean_metadata(metadata: dict, indent: int = 0) -> None:
    """
    오디오의 정제된 메타데이터를 계층적 구조로 출력하는 함수
    :param
        metadata(dict): 출력할 메타데이터 딕셔너리. 중첩된 구조를 가질 수 있음
    :param
        indent (int, optional): 중첩된 구조용 들여쓰기 수준(공백 개수). 기본값은 0
    :return:
        None: 메타데이터를 콘솔에 출력

    example:
        metadata = {
            "audio": {
                "index": 0,
                "codec": "mp3"
            }
        }
        출력결과:
        ----------
        audio.mp3:
            index: 0
            codec: mp3
        ----------
    """
    print("-" * 10)
    if isinstance(metadata, dict):  # isinstance = 값이 딕셔너리인지 확인하는 메서드
        for key, value in metadata.items():
            print(" " * indent + f"{key}: ", end="")
            if isinstance(value, dict):  # isinstance = 값이 딕셔너리인지 확인하는 메서드
                print_clean_metadata(value, indent=indent + 4)  # 재귀 호출로 하위 딕셔너리 출력
            else:
                if value:
                    print(value)  # 줄바꿈 포함.
    print("-" * 10)
#
# def raw_meatadata(metadata: dict, audio_title: str) -> None:
#     """
#     오디오의 raw 메타데이터를 출력
#     :param metadata:
#     :param audio_title:
#     :return:
#     """
#     print(f"\n\nraw metadata:\ntitle:{audio_title}\n{metadata}")