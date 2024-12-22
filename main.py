from utils import list_audio_files
from sound_manager import get_audio_metadata, save_metadata_json, update_metadata_json, del_metadata_json
from select_interface import get_and_print_audio_files, pretty_print_dict
import os

def main():
    # 1. 디렉토리 경로 입력받기

    while True:
        print("\n\nSound Library")
        print("1. 오디오 파일 전체 탐색")
        print("2. 오디오 파일 1개 메타데이터 보기") # New!
        print("3. 오디오 파일 1개 메타데이터 관리") # New!
        print("0. 종료")
        choice = input("선택하세요:" )

        # 1. 사운드 파일 탐색
        if choice == "1":
            # directory = input("오디오 파일이 있는 디렉토리 경로를 입력하세요: ")
            directory = "C:\projects\sound_lib01\sounds"
            # 2. list_audio_file 호출 -> 오디오 파일 목록 가져오기
            audio_files = get_and_print_audio_files(directory)
            if not audio_files:
                continue  # 반복문으로 돌아감
            # 5. for 루프: 오디오 파일마다 메타데이터 추출
            for audio_file in audio_files:
                file_path = os.path.join(directory, audio_file)
                get_audio_metadata(file_path)

        #2. Audio file 목록 출력
        elif choice == "2":
            # directory = input("오디오 파일이 있는 디렉토리 경로를 입력하세요: ")
            directory = "C:\projects\sound_lib01\sounds"
            # 2. list_audio_file 호출 -> 오디오 파일 목록 가져오기
            audio_files = get_and_print_audio_files(directory)
            # 사용자가 메타데이터를 조회할 파일을 선택하게 하기.
            file_index = input("\n조회할 파일 번호를 선택하세요: ")

            try:
                selected_file = audio_files[int(file_index) - 1]
                file_path = os.path.join(directory, selected_file)
                get_audio_metadata(file_path)
                """
                # for 문의 리스트 컴프리헨션
                # 파일 이름과 확장자 출력
                print(f"\n선택한 파일: {selected_file[-3:]}")
                # metadata_dict에서 codec 관련 키 출력
                codec = None # 초기화
                for key in metadata_dict:
                    if 'codec' in key: # key에 'codec'이 포함된 키만 처리
                        codec = metadata_dict[key] # 해당 값을 가져온다.
                        print(f"{key} : {metadata_dict[key]}") # key와 value 출력
                # codec이 존재하면 출력, 없으면 '정보 없음' 출력
                print(f"코덱: {codec if codec else '정보 없음'}")
                
                codec = next((metadata_dict[key] for key in metadata_dict if 'codec' in key), None)
                
                next()는 리스트 컴프리헨션으로 생성된 값을 차례대로 반환함.
                next()의 2번째 인자는 기본값 설정 부분, 만약 'codec'이 포함된 키가 없을 경우 None을 반환
                'codec' in key 조건을 만족하는 첫번째 키에 해당하는 값을 바로 갖져온다.
                """
            except (ValueError, IndexError) as e: # ValueError나 IndexError가 발생했을 때만 처리
                print(f"Error: {e}")

        elif choice == "3":
            print("메타데이터 관리")
            directory = "C:\projects\sound_lib01\sounds"
            audio_files = list_audio_files(directory)

            if audio_files:
                print("\n오디오 파일: ")
                for i, audio_file in enumerate(audio_files, start=1):
                    print(f"{i}. {audio_file}")

                # 사용자가 메타데이터를 조회할 파일을 선택하게 하기.
                file_index = input("관리할 파일 번호를 선택하세요: ")
                print("-" * 10)
                try:
                    # 파일 목록
                    selected_file = audio_files[int(file_index) - 1]
                    print(f"\n선택한 파일: {selected_file}")

                    file_path = os.path.join(directory, selected_file)
                    metadata_dict = get_audio_metadata(file_path)
                    metadata_manage = input("\n\n해당 오디오의 메타데이터를 어떻게 관리하시겠습니까?\nsave : 저장\nupdate : 수정\ndel : 삭제\n>>>")

                    if metadata_manage == "save":
                        save_metadata_json(metadata_dict)

                    elif metadata_manage == "update":
                        update_metadata_json(metadata_dict)
                        pretty_print_dict(metadata_dict)

                    elif metadata_manage == "del":
                        del_metadata_user_answer = input('key / field >>>')

                        if del_metadata_user_answer == "key":
                            select_del_file = input('삭제할 key 입력 >>> ')
                            del_metadata_json(delete_file=f"{select_del_file}")

                        elif del_metadata_user_answer == "field":
                            select_del_key = input('삭제할 필드 입력 >>> ')
                            del_metadata_json(delete_key=f"{select_del_key}")

                        else:
                            print("잘못 입력되었습니다. 다시 선택해주세요. ")
                    else:
                        print("잘못 입력되었습니다. 다시 선택해주세요. ")
                except (ValueError, IndexError) as e: # ValueError나 IndexError가 발생했을 때만 처리
                    print(f"Error: {e}")

            else:
                print("\n탐색된 파일이 없습니다.")

        elif choice == "0":
            print("종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()