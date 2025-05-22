from rag_tool import RAGSearchTool
from tools.finance_tool import FinanceNewsTool
from agents.supervisor_agent import SupervisorAgent

rag_tool = RAGSearchTool()
finance_tool = FinanceNewsTool()
supervisor_agent = SupervisorAgent()

async def run_router(input_text: str) -> str:
    return await supervisor_agent.invoke(input_text)
