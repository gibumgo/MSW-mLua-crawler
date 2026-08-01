import os

class ConfigManager:
    BASE_URL = "https://maplestoryworlds-creators.nexon.com/ko/docs/?postId="
    INPUT_FILE = "post_ids.txt"
    OUTPUT_DIR = "output"

    @classmethod
    def get_output_dir(cls) -> str:
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
        return cls.OUTPUT_DIR
