from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WikipediaLoader, TextLoader, UnstructuredFileLoader,WhatsAppChatLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil
c_path = r"chroma"


embedding_function = HuggingFaceEmbeddings(model_name = "BAAI/bge-base-en-v1.5")
loader = DirectoryLoader(r"Chat names", glob="*.txt", loader_cls=WhatsAppChatLoader)
docs = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
chunks = text_splitter.split_documents(docs)
if os.path.exists(c_path):
    shutil.rmtree(c_path)
#db = Chroma.from_documents(documents=docs, embedding=embedding_function, persist_directory=c_path)
db = Chroma(embedding_function=embedding_function, persist_directory=c_path)
def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks
    # Calculate Page IDs.
chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
existing_items = db.get(include=[])  # IDs are always included by default
existing_ids = set(existing_items["ids"])
print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
new_chunks = []
for chunk in chunks_with_ids:
    if chunk.metadata["id"] not in existing_ids:
        new_chunks.append(chunk)
MAX_BATCH_SIZE = 5461
if len(new_chunks):
    
    new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    # Dodavanje dokumenata u batch-ovima
    for i in range(0, len(new_chunks), MAX_BATCH_SIZE):
        batch = new_chunks[i:i + MAX_BATCH_SIZE]
        batch_ids = [chunk.metadata["id"] for chunk in batch]
    
        print(f"👉 Adding batch of {len(batch)} documents")
        db.add_documents(batch, ids=batch_ids)
else:
    print("✅ No new documents to add")
data_path =r"Chat names"
#db.add_documents(documents=docs)
db.persist()