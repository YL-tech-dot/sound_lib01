# 전역 설정값 constants.py 외부 파일로 분리
SUPPORTED_FORMATS = (".mp3", ".wav", ".flac", ".ogg")
FFPROBE_CMD = ["ffprobe", "-v", "error", "-show_streams", "-of", "json"]
INDENT_SIZE = 4
MAX_RECURSION_DEPTH = 10