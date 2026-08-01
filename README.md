# MSW-mLua-Crawler

## 📖 제작 배경 (Background)

본 프로젝트는 **메이플스토리 월드(MapleStory Worlds)** 게임 개발에 앞서, 팀 내 **mLua 코드 컨벤션**을 확립하기 위해 제작되었습니다.

공식 개발자 가이드를 크롤링하여 마크다운(Markdown) 형태로 문서화하며, 다음 두 가지 목적을 가집니다:

- **mLua 문법 이해**: 기본 루아(Lua)와 차별화되는 mLua의 스크립트 특성, 프로퍼티, 이벤트 핸들러 등의 문법을 분석합니다.
- **'이펙티브(Effective) mLua' 가이드라인 정립**: 멀티플레이어 환경에서의 데이터 동기화(Sync/TargetUserSync), 실행 공간 제어(ExecSpace), 성능 최적화 관련 항목을 수집하고 아카이브합니다.

---

## 🚀 주요 기능 (Features)

- **`post_ids.txt` 기반 일괄 크롤링**: 수집할 문서의 `postId` 목록을 텍스트 파일에 한 줄씩 기입하면, 해당 목록을 순회하며 문서를 자동으로 수집합니다.
- **표준 라이브러리 기반 HTTP 요청**: 별도의 `requests` 패키지 없이 Python 내장 `urllib.request`를 사용하여 HTML을 가져옵니다.
- **메타 태그 기반 마크다운 추출**: SPA 구조의 페이지에서 `<meta name="description">` 태그에 삽입된 원본 마크다운 본문을 직접 추출합니다.
- **링크 줄바꿈 최적화**: `[텍스트](URL)` 형식으로만 이루어진 줄에 한정하여 `<br>` 태그를 자동 주입합니다. GitHub, VSCode 등 다양한 마크다운 렌더러에서 링크들이 한 줄로 뭉치는 현상을 방지합니다.
- **파일명 정규화**: 파일 시스템에서 허용되지 않는 특수 문자를 제거하고, `{postId}_{제목}.md` 형식으로 결과물을 `output/` 폴더에 저장합니다.

---

## 🏗 모듈 구성 (Architecture)

| 파일 | 클래스 | 역할 |
|---|---|---|
| `config.py` | `ConfigManager` | 크롤링 대상 Base URL, 입력 파일 경로, 출력 폴더 경로 등 전역 설정값 관리 |
| `target_reader.py` | `TargetReader` | `post_ids.txt`를 읽어 수집 대상 ID 목록(`List[str]`)을 반환 |
| `crawler.py` | `Crawler` | `urllib.request`를 통해 대상 URL의 HTML을 가져옴 |
| `parser.py` | `Parser` | HTML에서 제목(`<title>`)과 마크다운 본문(`<meta name="description">`)을 파싱하고 후처리 |
| `file_writer.py` | `FileWriter` | 파싱된 마크다운 내용을 `output/` 디렉토리에 `.md` 파일로 저장 |

---

## 🛠 사용 방법 (Usage)

### 1. 환경 설정 및 요구 사항

**Python 3** 환경이 필요합니다. 가상 환경(`venv`) 활성화 후 아래 명령어로 의존성 패키지를 설치합니다.

```bash
# HTML 파싱 라이브러리 설치 (HTTP 요청은 Python 내장 urllib 사용)
pip install beautifulsoup4
```

### 2. 수집 대상 설정

프로젝트 루트의 `post_ids.txt` 파일에 수집할 문서의 `postId`를 한 줄에 하나씩 입력합니다.

```
1287
1288
1291
```

> Base URL(`https://maplestoryworlds-creators.nexon.com/ko/docs/?postId=`)에 각 ID가 붙어 요청 URL이 구성됩니다.

### 3. 스크립트 실행

메인 스크립트를 실행합니다.

```bash
python main.py
```

*(Mac 환경이거나 파이썬 환경 설정에 따라 `python3 main.py`를 사용하세요.)*

### 4. 결과물 확인

실행이 완료되면 `output/` 폴더에 `.md` 파일들이 생성됩니다.

```
output/
├── 1287_mLua.md
├── 1288_Script.md
└── ...
```

생성된 파일은 팀 내 학습 자료 또는 프로젝트 저장소의 Wiki 등으로 활용할 수 있습니다.
