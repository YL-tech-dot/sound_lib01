# metadata.py
import os
import subprocess
import json
from module.interface import print_metadata, print_clean_metadata  # 메타데이터 출력 함수


class Metadata:
    def __init__(self, audios_directory: str | bytes):
        """
        Metadata 클래스 초기화
        :param audios_directory: 오디오 파일 디렉토리 경로
        """
        self.audios_directory = audios_directory

    # Private 내부에서만 사용하는 함수이므로 은닉 함수로 전환
    def _handle_save(self, audio_directory, json_file_path: str) -> None:
        """메타데이터 저장
        :param json_file_path 저장할 오디오 파일의 메타데이터 파일명
        """
        metadata = self.read_audio_metadata(audio_directory, audio_title=audio_directory)
        self.create_metadata_json(metadata, json_file_path)

    def _handle_update(self, audio_directory, json_file_path: str) -> None:
        """
        메타데이터 수정
        :param audio_directory: 선택된 오디오 경로
        :param json_file_path: 저장된 오디오 파일의 메타데이터 파일명
        """
        self.update_metadata_json(audio_directory, json_file_path)

    def _handle_delete(self, json_file_path: str) -> None:
        """
        메타데이터 삭제
        :param json_file_path 저장된 오디오 파일의 메타데이터 파일
        """
        self.delete_metadata_json(json_file_path)

    def process_metadata(self, audio_directory: str, action: str, json_file_path: str) -> None:
        """
        메타데이터 작업 처리
        :param audio_directory: 선택된 오디오 경로
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
            handler(audio_directory, json_file_path)
            # self._handle_update(audio_directory, json_file_path)
            # self._handle_save(audio_directory, json_file_path)
        elif action == 'del':
            handler(json_file_path)  # self._handle_delete(json_file_path)

    @staticmethod
    def read_audio_metadata(audio_directory: str, audio_title: str) -> dict:
        """
        오디오 메타데이터 추출
        :param audio_directory : 오디오 파일 경로
        :param audio_title : 오디오 명
        :return dict: 오디오 메타데이터를 포함하는 dictionary
        """
        cmd = ["ffprobe", "-v", "error", "-show_streams", "-of", "json", audio_directory]
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
            print_metadata(metadata, audio_title=audio_title)
            return metadata

        except json.JSONDecodeError:
            print("ffprobe 출력 데이터를 JSON으로 변환하는 데 실패했습니다.")
            return {}

    # 메타데이터를 json 파일로 저장하는 함수
    @staticmethod
    def create_metadata_json(metadata: dict, json_file_path: str) -> None:
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
            print_clean_metadata(existing_data)  # 결과 발표
        except IOError as e:
            print(f"파일 쓰기 오류: {e}")

    @staticmethod
    def update_metadata_json(audio_directory: str, json_file_path: str) -> None:
        """
        메타데이터를 JSON 파일로 수정하는 함수
        :param audio_directory: 1개의 오디오 파일 경로
        :param json_file_path: 메타데이터가 저장된 JSON 파일 경로
        :return: None
        """
        # audio directory 통해서 메타데이터  한번 읽어주고
        metadata = Metadata.read_audio_metadata(audio_directory, audio_title=audio_directory)

        if not metadata:
            print("오디오에서 메타데이터를 찾을 수 없습니다.")
            return

        if not isinstance(metadata, dict):
            print("오디오의 메타데이터가 올바른 형식이 아닙니다.")
            return

        # 기존에 저장된 메타데이터 존재 여부 : 없는 경우
        if not os.path.exists(json_file_path):
            print(f"{audio_directory}의 메타데이터가 저장된 {json_file_path} 파일이 존재하지 않습니다.")
            return

        # 메타데이터 신규 저장
        with open(json_file_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # 메타데이터 출력 및 수정 시작
        print_clean_metadata(metadata)  # 메타데이터 출력

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

    def crud(self: 'Metadata', audio_directory) -> None:  # class type으로 변경
        """
        main.py 오디오의 메타데이터 관리 및 CRUD함수를 호출하는 함수
        :param: self(str): Metadata 클래스의 인스턴스
        :param: audio_directory : 오디오 1개 파일 경로
        :return: None
        """
        print("\n\n<메타데이터 관리>")
        # 사용자 선택
        metadata_action = input("저장(save) / 수정(update) / 삭제(del): ")
        json_file_path = f"{input('메타데이터 파일(JSON) 경로: ').strip()}.json"
        self.process_metadata(audio_directory, metadata_action, json_file_path)
