# pyrefly: ignore [missing-import]
import pytest
from bs4 import BeautifulSoup
from parser import Parser

@pytest.fixture
def parser():
    return Parser()

def test_extract_title(parser):
    html = "<title>mLua: MapleStory Worlds - Guide</title>"
    soup = BeautifulSoup(html, "html.parser")
    title = parser._extract_title(soup)
    assert title == "mLua"

def test_extract_title_none(parser):
    html = "<div>No title here</div>"
    soup = BeautifulSoup(html, "html.parser")
    title = parser._extract_title(soup)
    assert title is None

def test_extract_raw_markdown(parser):
    long_content = "This is a very long markdown content that should definitely exceed the fifty characters minimum length limit."
    html = f'<meta name="description" content="{long_content}">'
    soup = BeautifulSoup(html, "html.parser")
    markdown = parser._extract_raw_markdown(soup)
    assert markdown == long_content

def test_extract_raw_markdown_short_ignored(parser):
    short_content = "Too short"
    html = f'<meta name="description" content="{short_content}">'
    soup = BeautifulSoup(html, "html.parser")
    markdown = parser._extract_raw_markdown(soup)
    assert markdown is None

def test_clean_toastui_attributes(parser):
    content = 'Here is a link {"target":"_blank"} and some text.'
    cleaned = parser._clean_toastui_attributes(content)
    assert cleaned == 'Here is a link  and some text.'

def test_format_markdown_links(parser):
    content = "[Link](http://example.com)\nRegular text\n[Another Link](http://test.com)"
    formatted = parser._format_markdown_links(content)
    assert formatted == "[Link](http://example.com)<br>\nRegular text\n[Another Link](http://test.com)<br>"

def test_parse_and_convert(parser):
    html = """
    <html>
        <head>
            <title>mLua: Title</title>
            <meta name="description" content='A very long content that exceeds fifty characters.
[Link](http://example.com){"target":"_blank"}'>
        </head>
    </html>
    """
    title, markdown = parser.parse_and_convert(html)
    assert title == "mLua"
    assert "A very long content that exceeds fifty characters." in markdown
    assert "[Link](http://example.com)<br>" in markdown
