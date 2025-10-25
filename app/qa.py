
import os
import google.generativeai as genai
from app.embeddings import embed_text
from app import retriever

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("Please set GEMINI_API_KEY in your environment")
genai.configure(api_key=GEMINI_API_KEY)

GENERATE_MODEL = os.environ.get('GENERATE_MODEL', 'gemini-1.5-mini')
VECTOR_DIM = int(os.environ.get('VECTOR_DIM', 1536))

# initialize a vectorstore instance (will be populated by ingest)
vectorstore = retriever.VectorStore(dim=VECTOR_DIM)

def answer_query(query: str, top_k: int = 5) -> str:
    qvec = embed_text(query)
    ids = vectorstore.search(qvec, k=top_k)
    context = "\n\n".join(retriever.get_doc_text(i) for i in ids)
    prompt = f"""You are a helpful assistant. Use the context to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"""
    resp = genai.generate(model=GENERATE_MODEL, prompt=prompt, max_output_tokens=400)
    try:
        return resp.candidates[0].content
    except Exception:
        return str(resp)
