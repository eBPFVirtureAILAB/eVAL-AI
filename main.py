from langchain_community.chat_models import ChatOllama
from fastapi import FastAPI
from langserve import add_routes

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import PyMuPDFLoader
from langchain.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

# PDF 파일에서 문서를 로드합니다.
pdf_loader = PyMuPDFLoader("your_document.pdf")
documents = pdf_loader.load()

# Llama 임베딩을 사용하여 문서를 임베딩합니다.
class LlamaEmbeddings:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)

embedding_model = LlamaEmbeddings()
persist_directory = "chroma_db"  # 데이터를 저장할 디렉토리

# ChromaDB에 문서를 임베딩합니다.
vectorstore = Chroma(embedding_function=embedding_model.embed, persist_directory=persist_directory)
vectorstore.add_documents(documents)

# 데이터를 디스크에 저장합니다.
vectorstore.persist()

# RAG 체인을 생성합니다.
llm = ChatOllama(model="llama3:latest")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, professional assistant named namebot. Introduce yourself first, and answer the questions. Answer me in English no matter what."),
    ("user", "{input}")
])
chain = ConversationalRetrievalChain.from_llm_and_vectorstore(
    llm=llm,
    vectorstore=vectorstore,
    prompt=prompt
)

# FastAPI 앱을 생성하고 라우트를 추가합니다.
app = FastAPI()
add_routes(app, chain)

@app.post("/query")
async def query(input_text: str):
    result = chain.invoke({"input": input_text})
    return {"response": result}

# 샘플 쿼리를 실행합니다.
for token in chain.stream(
    {"input": "What is stock?"}
):
    print(token, end="")
