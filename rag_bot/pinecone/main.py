from dotenv import load_dotenv
load_dotenv()
from pinecone.grpc import PineconeGRPC as Pinecone
from sentence_transformers import SentenceTransformer
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..constants import EMBEDDING_MODEL, VECTOR_THRESHOLD

pc = Pinecone()
model = SentenceTransformer(EMBEDDING_MODEL)

########### SPLITTING ###########

def get_chunks(chunks: list[str], text_splitter: RecursiveCharacterTextSplitter) -> list[str]:
    # base splitting
    text = "\n---\n".join(chunks)
    chunks = text_splitter.split_text(text)
    # merging smaller chunks
    new_chunks = []
    chunk = ""
    for i, text in enumerate(chunks):
        
        chunk += text
        if len(chunk) > 200:
            new_chunks.append(chunk)
            chunk = ""
        elif (i+1)==len(chunks) and len(chunk) <= 200:
            # if the last chunk is small, appended to previous chunk
            new_chunks[-1] += chunk
            chunk = ""
        else:
            chunk += '\n\n'

    if chunk:
        new_chunks.append(chunk)
    return new_chunks

########### UPSERT ###########

def upsert_chunks(
        chunks: list[str], 
        index: Pinecone, 
        model: SentenceTransformer, 
        namespace: str, 
        metadata: dict
        ) -> None:

    vectors = []
    for chunk in chunks:
        metadata['data'] = chunk
        dense_vector = model.encode(chunk)
        vectors.append({
                'id': str(uuid.uuid4()),
                'values': dense_vector,
                'metadata': metadata
                })
    batch = 0
    while True:
        if batch == len(chunks):
            break
        i = batch
        batch = min([len(chunks), batch + 200])
        vector_batch = vectors[i:batch]
        upsert_response = index.upsert(
            vectors=vector_batch,
            namespace=namespace
        )
        print(upsert_response)


########## FETCHING ##########

def _get_context_list(query_response) -> str:

    print(f"---> Scores: {[item['score'] for item in query_response['matches']]}")
    context_list = [item['metadata']['data'] for item in query_response['matches'] if item['score']>VECTOR_THRESHOLD]
    print(f"---> Number of chunks with score > {VECTOR_THRESHOLD}: {len(context_list)}")
    return "\n---\n".join(context_list)


def fetch_context(user_query: str, index_name: str, namespace: str) -> str:
    index = pc.Index(index_name)
    dense = model.encode(user_query)    
    query_response = index.query(
        top_k=10,
        vector=dense,
        include_metadata=True,
        namespace=namespace
    )
    context = _get_context_list(query_response)
    return context