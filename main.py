# 이건 relpath네요
# 이거 이렇게 하는 거 아님

# 개같은 검색 이후에 알아낸 거
# 상대 주소에서 다른 놈이 해당 디렉토리 사용할 때 __init__.py를 통해 해당 위치에
# 패키지가 있음을 python에게 제안할 수 있음

# 저번에 이거 안 했다가 터진 경험 있어서 말합니다.
# (python 패키지 두 개 만들어서 터뜨린 경험이 있음)
from utils import list_audio_files
from sound_manager import get_audio_metadata, metadata_management
from select_interface import get_and_print_audio_files

# 이건 종속이고
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, PathCompleter
import os

# 반복되는 raw값은 코드의 가독성을 불안하게 해요.
SUGGESTING_DEFAULT_SHIT = "./sounds"

# FileCompleter 클래스 정의
# 얜 뭐지
# 심지어 이거 쓴 적도 없네요 
# 어따 쓰려고 만드셨나요
# 말이 없는 거 보니 기억이 안 나시거나 제가 연결이 끊겼거나 둘 중 하나겠네요
# 확인해 볼ᄁᆞ
class FileCompleter(Completer):
    def __init__(self, DIRECTORY):
        self.DIRECTORY = DIRECTORY
        
    # 어우 마법 진짜 개많네
    # yield가 있는 거 보면 비동기 같은데
    # Genearator 타입인가 뭔가가 지금 Task 혹은 Promise하는 놈인 건가
    # 저기에서 지금 상황이 웃긴 거는 document가 무슨 타입인지 알 수 없다는 거임
    # 
    # document: Document라 적혀 있는데 막상 똑같이 따라 쳐 보면
    # "Document" is not definedPylancereportUndefinedVariable
    # 
    # 본인이 무슨 자료형을 사용하고 있는지는 알고 계셔야 합니다
    # 적어 오세요
    def get_completions(self, document , complete_event):
        # 입력된 부분에 맞는 파일 및 디렉토리 목록을 반환
        for filename in os.listdir(self.DIRECTORY):
            if filename.startswith(document.text):  # 입력된 텍스트와 일치하는 항목만 필터링
                yield Completion(filename, start_position=-len(document.text))


# 경로를 입력받는 함수
def get_DIRECTORY_input(default_DIRECTORY):
    # PathCompleter를 사용하여 자동 완성 기능을 제공
    completer = PathCompleter(expanduser=True)

    # 기본 디렉토리 경로 설정
    session = PromptSession(completer=completer)

    # 기본 경로를 제공하여 입력받기
    # 여기서 default_DIRECTORY를 굳이 두 번 보여 줄 필요가 있을까요 저는 빼도 된다 생각하는데
    DIRECTORY_input = session.prompt(f"오디오 파일 경로를 입력하세요: ", default=default_DIRECTORY)
    
    # 이걸 사용하고 있는 이유는 아마 Path 문자열 처리를 힘으로 하고 계시기 때문이겠죠?
    # 저희에게는 pathlib라는 개쩌는 놈이 있습니다. 구글링해 보십시오. 이거 심지어 기본제공이에요
    # 
    # 저는 힘으로 다 만든다 주의지만 제대로 엣지케이스 관리 못 하실 거면
    # 라이브러리 쓰는 게 제일 좋습니다. OS나 fs 관련일 수록 더더욱이
    # 
    # 저도 보십시오 GPU Driver를 제가 힘으로 처음부터 쓰고 있지는 않잖습니ᄁᆞ
    # 
    # 저거 스탈린시키니까 작동을 더 잘 하는 거 같습니다만
    # Windows에서 정 문제되면 본인이 라이브러리를 쓰든 preprocessor를 쓰든 하십시오
    # DIRECTORY_input = DIRECTORY_input.replace("/", "\\").replace("\\\\", "\\")  # '\'을 '\\'로 처리
    return DIRECTORY_input


def main():
    # 1. 디렉토리 경로 입력받기

    while True:
        print("\n\nSound Library")
        print("1. 오디오 파일 전체 탐색")
        print("2. 오디오 파일 1개 메타데이터 보기")
        print("3. 오디오 파일 1개 메타데이터 관리")
        print("0. 종료")
        choice = input("선택하세요:")

        # 1. 사운드 파일 탐색
        if choice == "1":
            # "자동 완성된 경로"를 넣을 거면 적어도 본인 위치를 확인할 수 있는 코드를 넣는 걸 추천드립니다.
            # "내가 여기에 있으니까 무조건 여기에 있겠지?"는 때려죽일 짓이에요
            # 본인이 지금 그거 하셨습니다.
            # 딱 좋은 거 있네요
            
            # 자 그래요 저기 보면 적어도 뭔가 sounds를 적으려는 시도를 하고 있긴 한데
            # 솔직히 굉장히 아름답다고 보기는 좀 어려워 보입니다.
            # 사실 생각해 보면 cwd고 뭐고 필요가 없습니다.
            # 저거 상대 경로 작동하잖아요 뭐하러 절대 경로 넣음 그죠?
            
            # 차라리 현재 디렉토리 위치를 보여 주고 싶다 하면 cwd로 보여 주고 넣든 그건 본인 마음입니다만
            DIRECTORY = get_DIRECTORY_input(SUGGESTING_DEFAULT_SHIT)  # 자동 완성된 경로 입력
            
            # 이건 또 뭐야
            audio_files = get_and_print_audio_files(DIRECTORY)
            if not audio_files:
                continue  # 반복문으로 돌아감
            print("\n===Start===")
            for audio_file in audio_files:
                file_path = str(os.path.join(DIRECTORY, audio_file))  # type을 명시적으로 str로 캐스팅
                get_audio_metadata(file_path, audio_file)
            print("===End===\n")

        # 2. Audio file 목록 출력
        elif choice == "2":
            # 이거 또 시작이네
            # 차라리 매직 넘버를 쓰십시오
            # 보통 데이터가 mutable할 필요가 없으면 그냥 다 대문자로 쓰는 거도 방법입니다.
            # 네. const 쓰시라고요.
            # 지금 무지성으로 directory 그냥 다 대문자로 바꿔도 별 문제 없이 동작하는 거 보면
            # 너무 많은 걸 mutable하게 만들었다는 뜻이 될 수 있습니다.
            #
            # const를 많이 써 보는 건 님 데이터가 변하는지 마는지를 판단해 볼 수 있는 
            # 개쩌는 연습이 될 겁니다 ㅅㄱ
            DIRECTORY = get_DIRECTORY_input(SUGGESTING_DEFAULT_SHIT)
            audio_files = get_and_print_audio_files(DIRECTORY)
            file_index = input("\n조회할 파일 번호를 선택하세요: ")

            try:
                audio_file = audio_files[int(file_index) - 1]
                file_path = str(os.path.join(DIRECTORY, audio_file))
                get_audio_metadata(file_path, audio_file)

            except (ValueError, IndexError) as e:  # ValueError나 IndexError가 발생했을 때만 처리
                print(f"Error: {e}")

        # 3. Audio file 목록 출력
        elif choice == "3":
            print("메타데이터 관리")
            DIRECTORY = get_DIRECTORY_input(SUGGESTING_DEFAULT_SHIT)
            audio_files = list_audio_files(DIRECTORY)

            if audio_files:
                print("\n오디오 파일: ")
                for i, audio_file in enumerate(audio_files, start=1):
                    print(f"{i}. {audio_file}")
                file_index = input("관리할 파일 번호를 선택하세요: ")

                try:
                    selected_file = audio_files[int(file_index) - 1]
                    print(f"\n선택한 파일: {selected_file}")

                    file_path = str(os.path.join(DIRECTORY, selected_file))
                    metadata_management(file_path)

                except (ValueError, IndexError) as e:
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
