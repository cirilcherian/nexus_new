from langchain_openai import OpenAIEmbeddings
from common_utils.Config import Config

def default_embeddings():
    return OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)



