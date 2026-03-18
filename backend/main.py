from fastapi import FastAPI, UploadFile
# from rag.embed import embed_text
# from rag.retrieve import retrieve_chunks
# from rag.llm import generate_answer

app = FastAPI()

documents = []

# @app.post("/upload")
# async def upload(file: UploadFile):
#     text = (await file.read()).decode("utf-8")

#     embedding = embed_text(text)
#     documents.append({"text": text, "embedding": embedding})

#     return {"status": "uploaded"}

# @app.post("/query")
# async def query(data: dict):
#     query = data["query"]

#     query_embedding = embed_text(query)
#     chunks = retrieve_chunks(query_embedding, documents)

#     answer = generate_answer(query, chunks)

#     return {"answer": answer}