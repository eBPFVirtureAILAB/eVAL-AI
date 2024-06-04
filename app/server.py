from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain",
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

llm = ChatOllama(model="llama3:latest")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, professional assistant named namebot. Introduce yourself first, and answer the questions. answer me in english no matter what. "),
    ("user", "{input}")
])
chain = prompt | llm | StrOutputParser()

# Edit this to add the chain you want to add
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
