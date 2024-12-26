from utils import list_audio_files
from sound_manager import get_audio_metadata, save_metadata_json, update_metadata_json, del_metadata_json
import os

# Test Directory (Change this to your test directory path)
test_directory = "test_audio_files"
test_audio_file = os.path.join(test_directory, "sounds\deep-strange-whoosh-183845.mp3")  # Replace with an actual file
test_json_file = "metadata02.json"

# A. Test list_audio_files
print("Test: list_audio_files")
audio_files = list_audio_files(test_directory)
print("Found audio files:", audio_files)

# B. Test get_audio_metadata
print("\nTest: get_audio_metadata")
metadata = get_audio_metadata(test_audio_file)
print("Extracted Metadata:", metadata)

# C. Test save_metadata_json
print("\nTest: save_metadata_json")
save_metadata_json(metadata, test_json_file)

# D. Test update_metadata_json
print("\nTest: update_metadata_json")
new_metadata = {"test_audio2.mp3": {"duration": "300", "channels": 2}}
update_metadata_json(new_metadata, test_json_file)

# E. Test del_metadata_json
print("\nTest: del_metadata_json")
del_metadata_json(delete_key="test_audio2.mp3", file_name=test_json_file)

# F. Exception Handling
print("\nTest: Exception Handling")
try:
    list_audio_files("non_existent_dir")
except Exception as e:
    print("Caught exception:", e)