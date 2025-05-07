import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings



def load_documents(directory: str):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = os.path.join(directory, filename)
            loader = TextLoader(path)
            documents.extend(loader.load())
    return documents

def chunk_documents(documents):
    text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=10)
    return text_splitter.split_documents(documents)

def setup_chroma_db(chunks, collection_name="default", persist_directory=None):
    embeddings = OllamaEmbeddings(model="llama3")
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_directory
    )

def retrieve_context(collection, query, k=1):
    results = collection.similarity_search(query, k=k)
    return [doc.page_content for doc in results]



def get_magic_item_info(item_name: str):
    loader = TextLoader("data/dnd_magic_items.txt")
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="llama3")
    collection = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="magic_items",
        persist_directory="db/magic_items"
    )

    results = collection.similarity_search(item_name, k=2)
    return [doc.page_content for doc in results]
