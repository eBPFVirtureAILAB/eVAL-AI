from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

# FastAPI 앱 초기화
app = FastAPI()

# SentenceTransformer 모델 로드
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

# ChromaDB 클라이언트 초기화
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

try:
    chroma_client.delete_collection(name="qa_collection")
except Exception as e:
    print(f"컬렉션 삭제 중 오류 발생 (무시 가능): {e}")


# 컬렉션 가져오기 (없으면 새로 생성)
collection = chroma_client.get_or_create_collection(name="qa_collection")

df = pd.read_excel('qa_data.xlsx')

# 데이터를 컬렉션에 추가
collection.add(
    embeddings=[model.encode(q).tolist() for q in df['Question']],
    documents=df['Answer'].tolist(),
    ids=[f"id{i}" for i in range(len(df))]
)

class Query(BaseModel):
    text: str

@app.post("/chat")
async def chat(query: Query):
    # 쿼리 임베딩
    query_embedding = model.encode(query.text).tolist()
    
    # 가장 유사한 문서 검색
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    
    if results['distances'][0]:
        # 가장 유사한 응답 반환
        return {"response": results['documents'][0][0]}
    else:
        raise HTTPException(status_code=404, detail="적절한 응답을 찾을 수 없습니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200)