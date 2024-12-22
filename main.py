from sound_manager import list_audio_files, get_audio_metadata, save_metadata_json
import os

def main():
    # 1. 디렉토리 경로 입력받기

    while True:
        print("\n\nSound Library")
        print("1. 사운드 파일 탐색")
        print("2. 종료")
        choice = input("선택하세요:" )

        # 1. 사운드 파일 탐색
        if choice == "1":
            directory = input("오디오 파일이 있는 디렉토리 경로를 입력하세요: ")

            # 2. list_audio_file 호출 -> 오디오 파일 목록 가져오기
            audio_files = list_audio_files(directory)

            # 3. audio 목록 안내
            if audio_files:
                print("\n탐색된 사운드 파일: ")
                for i, audio_file in enumerate(audio_files, start=1):
                    print(f"{i}. {audio_file}") # 결과: [(1, "sound1.mp3"), (2, "sound2.wav")]

                # 3. 빈 딕셔너리(metadata_dict) 초기화
                metadata_dict = {}

                # 5. 저장한 데이터 불러오기
                """
                혹시 모를 기존에 
                json 파일을 읽고
                """
                save_metadata_json({}, "metadata.json")

                # 6, for 루프: 오디오 파일마다 메타데이터 추출
                for audio_file in audio_files:
                    file_path = os.path.join(directory, audio_file)
                    metadata = get_audio_metadata(file_path)

                    # 파일 이름을 키로, 메타데이터를 값으로 저장
                    metadata_dict[audio_file] = metadata

                # 6. 결과를 json 파일로 저장
                save_metadata_json(metadata_dict, "metadata.json")

                # 7. 처리 완료 메세지
                print(f"{len(audio_files)}개의 파일에 대한 메타데이터 처리가 완료되었습니다.")

            else:
                print("\n탐색된 파일이 없습니다.")

        elif choice == "2":
            print("종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")



if __name__ == "__main__":
    main()