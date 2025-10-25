
import os
import sys
from pathlib import Path
from uuid import uuid4
from tqdm import tqdm

from app.processors import text_processor, image_processor, audio_processor
from app.embeddings import embed_text
from app import retriever

CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

def process_file(path: Path, vectorstore: retriever.VectorStore):
    p = str(path)
    ext = path.suffix.lower()
    text = ""
    if ext == '.pdf':
        text = text_processor.extract_from_pdf(p)
    elif ext == '.docx':
        text = text_processor.extract_from_docx(p)
    elif ext == '.pptx':
        text = text_processor.extract_from_pptx(p)
    elif ext in ['.txt', '.md']:
        text = text_processor.extract_from_txt(p)
    elif ext in ['.png', '.jpg', '.jpeg']:
        text = image_processor.ocr_image(p)
    elif ext in ['.mp3', '.wav']:
        text = audio_processor.transcribe_audio(p)
    elif ext in ['.mp4', '.mkv']:
        audio_out = p + '.mp3'
        from app.processors.video_processor import extract_audio_from_video
        extract_audio_from_video(p, audio_out)
        text = audio_processor.transcribe_audio(audio_out)
    else:
        print(f"Skipping unsupported file: {p}")
        return

    if not text or text.strip() == "":
        print(f"No text extracted from {p}")
        return

    chunks = chunk_text(text)
    vecs = []
    metadatas = []
    for i, c in enumerate(chunks):
        emb = embed_text(c)
        vid = str(uuid4())
        vecs.append(emb)
        metadatas.append(vid)
        retriever.save_doc(vid, p, c, i)

    vectorstore.add(vecs, metadatas)

def ingest_folder(folder: str):
    retriever.init_db()
    dim = int(os.environ.get('VECTOR_DIM', 1536))
    vs = retriever.VectorStore(dim=dim)

    p = Path(folder)
    files = list(p.rglob('*'))
    for f in tqdm(files):
        if f.is_file():
            try:
                process_file(f, vs)
            except Exception as e:
                print(f"Error processing {f}: {e}")

    vs.save()
    print("Ingestion complete. FAISS index saved.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python app/ingest.py <folder_with_data>")
        sys.exit(1)
    ingest_folder(sys.argv[1])
