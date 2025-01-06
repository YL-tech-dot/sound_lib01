# main.py 진입점
import sys
from core import MenuHandler, MetadataHandler, file_utils
"""
    MenuHandler : 메뉴 선택지
    MetadataHandler : 메타데이터 관리
    file_utils : 
"""
def main():
    print("안녕하세요 오디오 라이브러리 관리 프로그램입니다.\nffprobe 설치여부를 확인하겠습니다.\n")
    check = file_utils.check_ffprobe()
    if not check:
        print("프로그램을 종료합니다.")
        return sys.exit(1)

    audios_dir = file_utils.get_directory_input()

    menu = MenuHandler(MetadataHandler(audios_dir),audios_dir=audios_dir)
    # 사용자가 탐색할 오디오 경로
    print("오디오 탐색을 시작하겠습니다.")
    # menu 탐색할 오디오 시작
    menu.show_menu()


if __name__ == "__main__":
    main()
