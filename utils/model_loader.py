import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from utils.config_loader import load_config
from langchain_groq import ChatGroq

#class to load embeddings model and LLM model
class ModelLoader:
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()

    #function to validate environment variables
    def _validate_env(self):
        required_vars = ['GROQ_API_KEY', 'HUGGINGFACE_TOKEN ']
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
    #function to load embedding model
    def load_embeddings(self):
        print("loading the embedding model")
        model_name = self.config["embedding_model"]["model_name"]
        return HuggingFaceEmbeddings(model_name = model_name)
    
    #function for loading llm
    def load_llm(self):
        print("Loading LLM model")
        model_name = self.config["llm"]["groq"]["model_name"]
        groq_model = ChatGroq(model = model_name, api_key = self.groq_api_key)
        print(groq_model.invoke("hi").content)

        return groq_model
    
        
