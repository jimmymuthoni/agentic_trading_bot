from pydantic import BaseModel
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict

class RagToolSchema(BaseModel):
    question: str

class QuestionRequest(BaseModel):
    question: str