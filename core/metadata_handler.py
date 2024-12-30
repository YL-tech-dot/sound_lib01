# metadata_handler.py
from constants import MAX_RECURSION_DEPTH  # 전역변수도 import로 불러올 수가 있다.
import os
import subprocess
import json

class MetadataHandler:
    def __init__(self, audios_dir):
        self.max_depth = MAX_RECURSION_DEPTH
        self.audios_dir = audios_dir

    def process_file(self, filepath: str) -> dict:
        # 메타데이터 처리 로직
        pass

    # Private 내부에서만 사용하는 함수이므로 은닉 함수로 전환
    def _handle_save(self, audio_dir, json_file_path: str) -> None:
        """메타데이터 저장
        :param json_file_path 저장할 오디오 파일의 메타데이터 파일명
        """
        metadata = self.read_audio_metadata(audio_dir, audio_title=audio_dir)
        self.create_metadata_json(metadata, json_file_path)

    def _handle_update(self, audio_dir, json_file_path: str) -> None:
        """
        메타데이터 수정
        :param audio_dir: 선택된 오디오 경로
        :param json_file_path: 저장된 오디오 파일의 메타데이터 파일명
        """
        self.update_metadata_json(audio_dir, json_file_path)

    def _handle_delete(self, json_file_path: str) -> None:
        """
        메타데이터 삭제
        :param json_file_path 저장된 오디오 파일의 메타데이터 파일
        """
        self.delete_metadata_json(json_file_path)

    def process_metadata(self, audio_dir: str, action: str, json_file_path: str) -> None:
        """
        메타데이터 작업 처리
        :param audio_dir: 선택된 오디오 경로
        :param action: 수행할 작업 (save/update/del)
        :param json_file_path: Json 파일 경로
        """
        actions = {
            'save': self._handle_save,
            'update': self._handle_update,
            'del': self._handle_delete
        }

        handler = actions.get(action)
        if action in ['update', 'save']:
            handler(audio_dir, json_file_path)
            # self._handle_update(audio_dir, json_file_path)
            # self._handle_save(audio_dir, json_file_path)
        elif action == 'del':
            handler(json_file_path)  # self._handle_delete(json_file_path)

    def read_audio_metadata(self, audio_dir: str, audio_title: str) -> dict:
        """
        오디오 메타데이터 추출
        :param audio_dir : 오디오 파일 경로
        :param audio_title : 오디오 명
        :return dict: 오디오 메타데이터를 포함하는 dictionary
        """
        cmd = ["ffprobe", "-v", "error", "-show_streams", "-of", "json", audio_dir]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # ffprobe 명령이 실패할 경우 subprocess.run의 result.stderr에 에러 메시지
        if result.returncode != 0:
            print(f"ffprobe 실행 실패: 파일 경로가 잘못되었거나 지원되지 않는 형식일 수 있습니다.\n{result.stderr}")
            return {}

        # JSON Parsing
        try:
            parsed_data = json.loads(result.stdout)
            streams = parsed_data.get("streams")
            # print(f"parsed_data:{parsed_data}")
            # print(f"parsed_data, type: {type(parsed_data)}")

            if not streams:
                print("스트림 정보가 없습니다. 오디오 파일인지 확인하세요.")
                return {}
            metadata = streams[0]
            self.print_metadata(metadata)
            return metadata

        except json.JSONDecodeError:
            print("ffprobe 출력 데이터를 JSON으로 변환하는 데 실패했습니다.")
            return {}

    # 메타데이터를 json 파일로 저장하는 함수
    def create_metadata_json(self, metadata: dict, json_file_path: str) -> None:
        """
        메타데이터를 json 파일로 저장하는 함수
        :param metadata: audio file's info
        :param json_file_path: 메타데이터 저장할 이름
        """
        # 기존 파일 존재 여부 확인
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, "r") as f:
                    existing_data = json.load(f)  # json 파일 내용 ( json -> dict )
                print("파일이 기존에 저장되어있습니다. 새로 덮어쓰시겠습니까?")
            except json.JSONDecodeError:
                print("기존 파일이 손상되었습니다.")
                return
            except IOError as e:
                print(f"파일 읽기 오류: {e}")
                return
        else:
            print("기존에 저장된 데이터가 없습니다.")
            existing_data = {}

        if input("계속하시겠습니까? (yes/no): ").strip().lower() != "yes":
            print("저장 취소")
            return
        # json 파일 저장하기
        try:
            existing_data[json_file_path] = metadata
            with open(json_file_path, "w") as f:
                json.dump(existing_data, f, indent=4)
            print("저장 완료")
            self.print_clean_metadata(existing_data)  # 결과 발표
        except IOError as e:
            print(f"파일 쓰기 오류: {e}")

    def update_metadata_json(self, audio_dir: str, json_file_path: str) -> None:
        """
        메타데이터를 JSON 파일로 수정하는 함수
        :param audio_dir: 1개의 오디오 파일 경로
        :param json_file_path: 메타데이터가 저장된 JSON 파일 경로
        :return: None
        """
        # audio directory 통해서 메타데이터  한번 읽어주고
        metadata = MetadataHandler.read_audio_metadata(audio_dir, audio_title=audio_dir)

        if not metadata:
            print("오디오에서 메타데이터를 찾을 수 없습니다.")
            return

        if not isinstance(metadata, dict):
            print("오디오의 메타데이터가 올바른 형식이 아닙니다.")
            return

        # 기존에 저장된 메타데이터 존재 여부 : 없는 경우
        if not os.path.exists(json_file_path):
            print(f"{audio_dir}의 메타데이터가 저장된 {json_file_path} 파일이 존재하지 않습니다.")
            return

        # 메타데이터 신규 저장
        with open(json_file_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # 메타데이터 출력 및 수정 시작
        self.print_clean_metadata(metadata)  # 메타데이터 출력

        # 수정할 key 찾기
        find_key = input("수정할 key를 입력하세요: ").strip()
        if find_key not in metadata:
            print(f"'{find_key}' 키가 존재하지 않습니다.")
            return
        # key를 찾았을 경우 값을 수정
        new_value = input(f"'{find_key}'의 새로운 값을 입력하세요: ").strip()
        metadata[find_key] = new_value

        # 수정된 메타데이터 저장
        try:
            with open(json_file_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=4)
            print(f"'{find_key}' 키가 '{new_value}'로 수정되었습니다.")

        except Exception as e:
            print(f"파일 저장 중 오류가 발생했습니다: {e}")

    @staticmethod
    def delete_metadata_json(json_file_path: str) -> None:
        """
        JSON 파일에서 특정 메타데이터 항목 또는 파일 이름 전체 삭제
        :param json_file_path: 메타데이터가 저장된 JSON 파일 이름
        :return: None
        """
        # 파일 존재 여부 확인
        if not os.path.exists(json_file_path):
            print(f"저장된 '{json_file_path}' 파일이 존재하지 않습니다.")
            return

        # 전체 파일 삭제 여부 확인
        delete_option = input("저장된 메타데이터 파일을 삭제하시겠습니까? (yes/no): ").strip().lower()
        if delete_option == "yes":
            try:
                os.remove(json_file_path)
                print(f"'{json_file_path}' 파일이 성공적으로 삭제되었습니다.")
            except OSError as e:
                print(f"파일 삭제 중 오류가 발생했습니다: {e}")
            return
        else:
            print("파일을 삭제하지 않고 진행합니다.")

    def crud(self, audio_dir) -> None:  # class type으로 변경
        """
        main.py 오디오의 메타데이터 관리 및 CRUD함수를 호출하는 함수
        :param: self(str): Metadata 클래스의 인스턴스
        :param: audio_dir : 오디오 1개 파일 경로
        :return: None
        """
        print("\n\n<메타데이터 관리>")
        # 사용자 선택
        metadata_action = input("저장(save) / 수정(update) / 삭제(del): ")
        json_file_path = f"{input('메타데이터 파일(JSON) 경로: ').strip()}.json"
        self.process_metadata(audio_dir, metadata_action, json_file_path)

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

    def print_clean_metadata(self, metadata: dict, indent: int = 0) -> None:
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
                    self.print_clean_metadata(value, indent=indent + 4)  # 재귀 호출로 하위 딕셔너리 출력
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
