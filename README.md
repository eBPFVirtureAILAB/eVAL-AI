
## 1. 환경 설정

### 1.1 필요 조건
- Docker
- Python 3.11 이상
- Poetry 1.6.1

### 1.2 프로젝트 구조
project/
│
├── app/
│   ├── server.py
│   ├── embed_pdf.py
│   └── chatbot.py
│
├── packages/
│   └── (필요한 패키지 파일들)
│
├── Dockerfile
├── pyproject.toml
├── poetry.lock
└── README.md

## 2. Docker 이미지 빌드 및 실행

### 2.1 Docker 이미지 빌드
터미널에서 다음 명령어를 실행하여 Docker 이미지를 빌드합니다:

~~~bash
docker build -t chromadb-chatbot .
~~~
2.2 Docker 컨테이너 실행
다음 명령어로 컨테이너를 실행합니다:
~~~bash
run -d -p 8080:8080 -v /path/to/your/pdfs:/code/pdfs chromadb-chatbot
~~~
/path/to/your/pdfs를 실제 PDF 파일이 있는 로컬 디렉토리 경로로 변경하세요.
3. PDF 데이터 임베딩
3.1 임베딩 스크립트 실행
컨테이너 내부에서 임베딩 스크립트를 실행합니다:
~~~bash 
exec -it [컨테이너_ID] poetry run python app/embed_pdf.py
~~~
이 스크립트는 /code/pdfs 디렉토리의 모든 PDF 파일을 읽고, 내용을 추출하여 ChromaDB에 임베딩합니다.
4. 챗봇 API 실행
4.1 API 서버 시작
임베딩이 완료되면, 챗봇 API 서버가 자동으로 시작됩니다. 서버는 8080 포트에서 실행됩니다.
4.2 API 사용
API를 테스트하려면 다음과 같이 curl 명령어를 사용할 수 있습니다:
~~~bash
-X POST "http://localhost:8080/chat" -H "Content-Type: application/json" -d '{"text":"당신의 질문"}'
~~~
5. 추가 작업
5.1 새로운 PDF 추가
새로운 PDF를 추가하려면:

호스트 시스템의 마운트된 디렉토리에 PDF 파일을 추가합니다.
임베딩 스크립트를 다시 실행합니다.

5.2 ChromaDB 데이터 백업
ChromaDB 데이터를 백업하려면 컨테이너의 /code/chroma_db 디렉토리를 호스트 시스템으로 복사하세요.
6. 문제 해결

컨테이너가 시작되지 않는 경우, Docker 로그를 확인하세요:
~~~bash 
logs [컨테이너_ID]
~~~

API에 연결할 수 없는 경우, 포트 매핑을 확인하세요.
임베딩 과정에서 오류가 발생하면, PDF 파일의 형식과 권한을 확인하세요.

