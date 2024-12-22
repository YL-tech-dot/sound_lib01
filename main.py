from sound_manager import list_audio_files, get_audio_metadata, save_metadata_json
import os

def main():
    # 1. 디렉토리 경로 입력받기

    while True:
        print("\n\nSound Library")
        print("1. 사운드 파일 탐색")
        print("2. 메타데이터 보기") # New!
        print("3. 종료")
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

        #2. Audio file 목록 출력
        elif choice == "2":
            directory = input("오디오 파일이 있는 디렉토리 경로를 입력하세요: ")
            audio_files = list_audio_files(directory)

            if audio_files:
                print("\n사운드 파일: ")
                for i, audio_file in enumerate(audio_files, start=1):
                    print(f"{i}. {audio_file}")

                # 사용자가 메타데이터를 조회할 파일을 선택하게 하기.
                file_index = input("조회할 파일 번호를 선택하세요: ")

                try:
                    selected_file = audio_files[int(file_index) - 1]
                    file_path = os.path.join(directory, selected_file)
                    metadata_dict = get_audio_metadata(file_path)

                    # 파일 이름과 확장자 출력
                    print(f"\n선택한 파일: {selected_file[-3:]}")

                    # 메타데이터 출력
                    print(f"길이: {float(metadata_dict['duration']):.2f}초")
                    print(f"채널 수: {metadata_dict['channels']}")
                    print(f"샘플링 주파수: {metadata_dict['sample_rate']}Hz")
                    print(f"비트레이트: {metadata_dict['bit_rate']}bps")


                    # metadata_dict에서 codec 관련 키 출력
                    codec = None # 초기화
                    for key in metadata_dict:
                        if 'codec' in key: # key에 'codec'이 포함된 키만 처리
                            codec = metadata_dict[key] # 해당 값을 가져온다.
                            print(f"{key} : {metadata_dict[key]}") # key와 value 출력

                    # codec이 존재하면 출력, 없으면 '정보 없음' 출력
                    print(f"코덱: {codec if codec else '정보 없음'}")

                    """
                    # for 문의 리스트 컴프리헨션
                    codec = next((metadata_dict[key] for key in metadata_dict if 'codec' in key), None)
                    
                    next()는 리스트 컴프리헨션으로 생성된 값을 차례대로 반환함.
                    next()의 2번째 인자는 기본값 설정 부분, 만약 'codec'이 포함된 키가 없을 경우 None을 반환
                    'codec' in key 조건을 만족하는 첫번째 키에 해당하는 값을 바로 갖져온다.
                    """

                    print(f"비트 깊이: {metadata_dict.get('bit_depth', '정보 없음')}")

                    print("-"*10)
                    print(metadata_dict)
                    print("-"*10)

                except (ValueError, IndexError) as e:
                    # print(f"error >>{e}")
                    # ValueError나 IndexError가 발생했을 때만 처리
                    print(f"Error: {e}")

            else:
                print("\n탐색된 파일이 없습니다.")

        elif choice == "3":
            print("종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")



if __name__ == "__main__":
    main()