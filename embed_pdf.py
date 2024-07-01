import sys
import chromadb
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def embed_pdf(pdf_path):
    # SentenceTransformer 모델 로드
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

    # ChromaDB 클라이언트 초기화
    chroma_client = chromadb.PersistentClient(path="/app/chroma_db")

    # 컬렉션 생성 또는 가져오기
    collection = chroma_client.get_or_create_collection(name="pdf_collection")

    # PDF에서 텍스트 추출
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(text)

    # 청크를 임베딩하고 ChromaDB에 저장
    collection.add(
        embeddings=[model.encode(chunk).tolist() for chunk in chunks],
        documents=chunks,
        ids=[f"{os.path.basename(pdf_path)}_chunk_{i}" for i in range(len(chunks))]
    )

    print(f"PDF '{pdf_path}' 임베딩 완료 및 저장됨")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python embed_pdf.py <pdf_file_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"오류: 파일 '{pdf_path}'를 찾을 수 없습니다.")
        sys.exit(1)

    embed_pdf(pdf_path)
