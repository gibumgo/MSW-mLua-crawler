import os
from typing import List

class TargetReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_post_ids(self) -> List[str]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"입력 파일({self.file_path})을 찾을 수 없습니다.")
        
        post_ids = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    post_ids.append(stripped)
        return post_ids
