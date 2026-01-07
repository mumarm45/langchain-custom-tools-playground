from langgraph.prebuilt import create_react_agent
from tools.tools import CustomTool
from dotenv import load_dotenv
from core.llm_client import LLMClient
load_dotenv()


class Agent:
    def __init__(self, prompt: str):
        self.llm_client = LLMClient()
        self.tools = CustomTool.get_tools()
        self.llm = self.llm_client.client
        self.prompt = prompt

    def create_agent(self):
        # CORRECT ORDER: LLM first, tools second
        return create_react_agent(model=self.llm, tools=self.tools, prompt=self.prompt)
    
    def run(self, query: str):
        """Run the agent with a query"""
        agent_executor = self.create_agent()
        result = agent_executor.invoke({"messages": [("user", query)]})
        return result
