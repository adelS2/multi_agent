# agents/__init__.py

class Agent:
    def __init__(self, name, instructions, tools=None, handoffs=None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.handoffs = handoffs or []

class Runner:
    @staticmethod
    def run(agent, input_items, context=None):
        query = input_items[-1]["content"]
        for tool in agent.tools:
            return type("Result", (), {
                "new_items": [MessageOutputItem(text=tool(query))]
            })()
        for handoff_agent in agent.handoffs or []:
            result = Runner.run(handoff_agent, input_items)
            if result:
                return result
        return type("Result", (), {"new_items": [MessageOutputItem(text="Keine Antwort.")]} )()

class MessageOutputItem:
    def __init__(self, text):
        self.text = text

class ToolCallOutputItem:
    def __init__(self, output):
        self.output = output

class ItemHelpers:
    @staticmethod
    def text_message_output(item):
        return getattr(item, "text", None) or getattr(item, "output", None)

def handoff(agent):
    return agent
