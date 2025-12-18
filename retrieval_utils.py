import os
import json
from PIL import Image as PILImage
import google.generativeai as genai
from llama_index.core.schema import ImageNode
from config import GOOGLE_API_KEY, GEMINI_MODEL_NAME

genai.configure(api_key=GOOGLE_API_KEY)

# QA prompt template
QA_TEMPLATE = (
    "Based on the provided information, including relevant images and retrieved context from the video, "
    "accurately and precisely answer the query without any additional prior knowledge.\n"
    "---------------------\n"
    "Context: {context_str}\n"
    "Metadata for video: {metadata_str}\n"
    "---------------------\n"
    "Query: {query_str}\n"
    "Answer: "
)

# Create retriever from index
def create_retriever(index, text_top_k=1, image_top_k=5):
    return index.as_retriever(similarity_top_k=text_top_k, image_similarity_top_k=image_top_k)

# Retrieve images and text
def retrieve(retriever_engine, query_str):
    retrieval_results = retriever_engine.retrieve(query_str)
    retrieved_image = []
    retrieved_text = []
    for res_node in retrieval_results:
        if isinstance(res_node.node, ImageNode):
            retrieved_image.append(res_node.node.metadata["file_path"])
        else:
            retrieved_text.append(res_node.text)
    return retrieved_image, retrieved_text

# Generate answer using Gemini
def generate_answer(query, context_text, metadata, image_paths):
    context_str = "\n\n".join(context_text)
    metadata_str = json.dumps(metadata)
    formatted_prompt = QA_TEMPLATE.format(context_str=context_str, metadata_str=metadata_str, query_str=query)
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    content = [formatted_prompt]
    for img_path in image_paths:
        if os.path.isfile(img_path):
            pil_image = PILImage.open(img_path)
            content.append(pil_image)
    try:
        result = model.generate_content(content)
        if result.candidates and result.candidates[0].content.parts:
            return result.text
        else:
            return "No answer generated. Try rephrasing your query."
    except Exception as e:
        return f"Error generating answer: {str(e)}"
