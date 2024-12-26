from huggingface_hub import login
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq

query = input()
model_kwargs = model_kwargs = {'device':'gpu', 'trust_remote_code': True}
encode_kwargs = {'normalize_embeddings': True}
model_path = r"paraphrase-multilingual-MiniLM-L12-v2"
c_path = r"chroma"
embedding_function = HuggingFaceEmbeddings(model_name = "BAAI/bge-base-en-v1.5")

db = Chroma(persist_directory=c_path, embedding_function=embedding_function)
context = db.similarity_search(query=query, k=15)







context_as_string = " ".join(doc.page_content for doc in context)
API_KEY = "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"

llm = Groq(
    api_key=API_KEY,
)
response = llm.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": query,
        },
        {
            "role": "system",
            "content": context_as_string+"Ti si chatbot koji prica na srpskom",
        }
    ],
    model="llama3-70b-8192",
)
print(response.choices[0].message.content)