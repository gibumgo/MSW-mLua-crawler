import os
import re

class FileWriter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def sanitize_filename(self, filename: str) -> str:
        """파일 이름으로 사용할 수 없는 문자를 제거합니다."""
        return re.sub(r'[\\/*?:"<>|]', "", filename)

    def write_markdown(self, filename: str, content: str) -> str:
        safe_filename = self.sanitize_filename(filename) + ".md"
        file_path = os.path.join(self.output_dir, safe_filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return file_path
