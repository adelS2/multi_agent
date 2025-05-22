
from tools.finance_tool import FinanceAnalysisTool
from agents import Agent

finance_agent = Agent(
    name="Finance Analysis Agent",
    instructions="Führe historische Kursanalysen und Prognosen für bekannte Aktienunternehmen durch.",
    tools=[FinanceAnalysisTool()]
)
