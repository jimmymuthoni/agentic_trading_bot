from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import AIMessage, HumanMessage
from typing_extensions import Annotated, TypedDict
from utils.model_loader import ModelLoader
from toolkit.tools import *
from typing import List

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

class GraphBuilder:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tools = [retiever_tool, financials_tools, tavilytool]
        llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.llm_with_tools = llm_with_tools
        self.graph = None

    def _chatbot_node(self, state:AgentState):
        return {"messages": [self.llm_with_tools.invoke(state['messages'])]}
    
    #bulding the graph
    def graph_building(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("chatbot", self._chatbot_node)
        tool_node = ToolNode(tools=self.tools)
        workflow.add_node("tools", tool_node)
        workflow.add_conditional_edges("chatbot", tools_condition)
        workflow.add_edge("tools", "chatbot")
        workflow.add_edge(START, "chatbot")
        self.graph = workflow.compile()

    def get_graph(self):
        if self.graph is None:
            raise ValueError("Graph not built. call build() first.")
        return self.graph
    

        
    
