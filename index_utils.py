from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from config import LANCEDB_URI, TEXT_TABLE_NAME, IMAGE_TABLE_NAME, EMBEDDING_MODEL_NAME

# Get embedding model
def get_embedding_model():
    return FastEmbedEmbedding(model_name=EMBEDDING_MODEL_NAME)

# Create vector stores
def create_vector_stores():
    text_store = LanceDBVectorStore(uri=LANCEDB_URI, table_name=TEXT_TABLE_NAME)
    image_store = LanceDBVectorStore(uri=LANCEDB_URI, table_name=IMAGE_TABLE_NAME)
    return text_store, image_store

# Create storage context
def create_storage_context(text_store, image_store):
    return StorageContext.from_defaults(vector_store=text_store, image_store=image_store)

# Load documents from folder
def load_documents(folder_path):
    return SimpleDirectoryReader(folder_path).load_data()

# Create multimodal index
def create_multimodal_index(documents, storage_context, embed_model):
    return MultiModalVectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

# Build complete index
def build_index(folder_path):
    embed_model = get_embedding_model()
    text_store, image_store = create_vector_stores()
    storage_context = create_storage_context(text_store, image_store)
    documents = load_documents(folder_path)
    index = create_multimodal_index(documents, storage_context, embed_model)
    return index
