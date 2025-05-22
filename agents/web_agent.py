from tools.web_tool import WebSearchTool
from agents import Agent

web_agent = Agent(
    name="Websuche Agent",
    instructions="Verwende Websuche, wenn Informationen aktuell oder onlinebasiert sind.",
    tools=[WebSearchTool()]
)
