# core/__init__.py
from .metadata_handler import MetadataHandler
from .menu_handler import MenuHandler
from .file_utils import validate_path, is_audio_file

# 마법의 전역변수 취급
__all__ = ['MetadataHandler', 'MenuHandler', 'validate_path', 'is_audio_file']