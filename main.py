from langchain_community.chat_models import ChatOllama
from fastapi import FastAPI
from langserve import add_routes

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatOllama(model="llama3:latest")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, professional assistant named namebot. Introduce yourself first, and answer the questions. answer me in english no matter what. "),
    ("user", "{input}")
])
chain = prompt | llm | StrOutputParser()
# d = chain.invoke({"input": "What is stock?"})
# print(d)



for token in chain.stream(
    {"input": "What is stock?"}
):
    print(token, end="")

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain",
)

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn

    # uvicorn: ASGI(Asynchronous Server Gateway Interface) 서버를 구현한 비동기 경량 웹 서버
    uvicorn.run(app, host="localhost", port=8000)