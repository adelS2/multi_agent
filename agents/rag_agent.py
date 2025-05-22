from tools.rag_tool import RAGSearchTool
from agents import Agent

rag_agent = Agent(
    name="RAG Agent",
    instructions="Nutze die Vektor-Datenbank für faktenbasierte Fragen über Unternehmen.",
    tools=[RAGSearchTool()]
)
