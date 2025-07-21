import os
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from data_models.models import RagToolSchema
from langchain_pinecone import PineconeVectorStore
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()

api_wraper = PolygonAPIWrapper()
model_loader = ModelLoader()
config = load_config()

#tool for retieving information from pineconedb
@tool(args_schema=RagToolSchema)
def retiever_tool(question):
    """This is a retiever tool for interacting with pinecone vector db"""
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    vector_store = PineconeVectorStore(index=pc.Index(config["vector_db"]["index_name"]), embedding=model_loader.groq_api_key())
    retriever = vector_store.as_retriever(
        search_type = "similarity_score_threshold",
        search_kwargs = {"k": config["retriever"]["top_k"], "score_threshold":config["retriever"]["score_threshold"]}

    )

    return retriever

tavilytool = TavilySearchResults(
    max_results = config["tools"]["tavily"]["max_results"],
    depth = "advanced",
    include_answers = True,
    include_raw_content = True,

)

financials_tools = PolygonFinancials(api_wrapper=api_wraper)