import re
from bs4 import BeautifulSoup
from typing import Tuple, Optional

class Parser:
    MINIMUM_MARKDOWN_LENGTH = 50

    def parse_and_convert(self, html: str) -> Tuple[Optional[str], Optional[str]]:
        """HTML을 받아 제목과 마크다운 본문을 반환합니다."""
        soup = BeautifulSoup(html, "html.parser")
        
        title = self._extract_title(soup)
        raw_markdown = self._extract_raw_markdown(soup)
        
        if not raw_markdown:
            return title, None
            
        cleaned_markdown = self._clean_toastui_attributes(raw_markdown)
        formatted_markdown = self._format_markdown_links(cleaned_markdown)
        
        return title, formatted_markdown

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        title_tag = soup.find("title")
        if not title_tag:
            return None
        
        title_text = title_tag.get_text(strip=True)
        return title_text.split(":")[0].strip()

    def _extract_raw_markdown(self, soup: BeautifulSoup) -> Optional[str]:
        meta_tags = soup.find_all("meta", {"name": "description"})
        
        for meta in meta_tags:
            content = meta.get("content", "")
            if content and len(content) > self.MINIMUM_MARKDOWN_LENGTH:
                return content
                
        return None

    def _clean_toastui_attributes(self, content: str) -> str:
        return re.sub(r'\{"target":"_blank"\}', '', content)

    def _format_markdown_links(self, content: str) -> str:
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            stripped = line.rstrip()
            if re.match(r'^\[.*\]\(.*\)$', stripped):
                formatted_lines.append(f"{stripped}<br>")
                continue
            formatted_lines.append(stripped)
                
        return '\n'.join(formatted_lines)
