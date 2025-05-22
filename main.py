from agents.supervisor_agent import supervisor_agent
from agents import MessageOutputItem, ToolCallOutputItem, ItemHelpers

def ask(question: str):
    result = supervisor_agent.run(question)

    for item in result.new_items:
        if isinstance(item, MessageOutputItem):
            print("✅ Antwort:", item.text)
        elif isinstance(item, ToolCallOutputItem):
            print("🔧 Tool-Antwort:", item.output)
        else:
            print("📤 Unbekanntes Ergebnis:", item)

if __name__ == "__main__":
    while True:
        frage = input("❓ Frage: ")
        if frage.strip().lower() in ["exit", "quit"]:
            break
        ask(frage)
