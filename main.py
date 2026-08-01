from config import ConfigManager
from target_reader import TargetReader
from crawler import Crawler
from parser import Parser
from file_writer import FileWriter

def main():
    config = ConfigManager()
    output_dir = config.get_output_dir()
    
    reader = TargetReader(config.INPUT_FILE)
    crawler = Crawler()
    parser = Parser()
    writer = FileWriter(output_dir)
    
    try:
        post_ids = reader.read_post_ids()
    except FileNotFoundError as e:
        print(f"오류: {e}")
        return

    for post_id in post_ids:
        url = f"{config.BASE_URL}{post_id}"
        print(f"[{post_id}] 크롤링 시작: {url}")
        
        try:
            html = crawler.get_html(url)
            title, markdown_content = parser.parse_and_convert(html)
            
            if title and markdown_content:
                # 제목을 파일 이름으로 사용하되, 고유성을 위해 post_id를 접두어로 추가
                filename = f"{post_id}_{title}"
                saved_path = writer.write_markdown(filename, markdown_content)
                print(f"[{post_id}] 성공적으로 저장되었습니다: {saved_path}")
            else:
                print(f"[{post_id}] 대상 요소를 찾을 수 없어 건너뜁니다.")
        except Exception as e:
            print(f"[{post_id}] 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
