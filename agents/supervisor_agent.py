from agents.rag_agent import rag_agent
from agents.web_agent import web_agent
from agents.finance_agent import finance_agent
from agents import Agent, handoff, Runner, MessageOutputItem
from qa_ethics_agent import qa_ethics_agent
import re

class SupervisorAgentWithFallback:
    def __init__(self):
        self.primary = Agent(
            name="Supervisor Agent",
            instructions="""Du bist ein Routing-Agent. Entscheide, welches Tool benutzt werden soll:

- 📚 RAGSearchTool → für Fakten/Jahresdaten
- 📊 TableSummaryTool → wenn Tabellen erwähnt werden
- 🔍 WebSearchTool → für aktuelle Infos, Kurse, Nachrichten

Wenn du unsicher bist, versuche zuerst RAG.
""",
            handoffs=[
                handoff(agent=rag_agent),
                handoff(agent=web_agent),
            ]
        )
        self.fallback = web_agent
        self.finance = finance_agent
        # NEU: Letzte Websuche-Umsatzdaten merken
        self.last_web_answer = None

    def run(self, query: str):
        from tools.diagram_from_text_tool import diagram_from_text_tool
        input_items = [{"role": "user", "content": query}]
        lower_query = query.lower()

        # Diagramm-Tool immer als ALLERERSTES prüfen!
        if any(w in lower_query for w in ["diagramm", "liniendiagramm", "balkendiagramm", "stelle", "darstellen", "visualisierung", "chart", "plot"]):
            if self.last_web_answer and re.search(r"20\d{2}[^\d]*\d+[\.,]?\d*[^\d]*(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", self.last_web_answer, re.IGNORECASE):
                print("📊 Erstelle Diagramm aus Websuche-Daten...")
                diagram_result = diagram_from_text_tool(self.last_web_answer)
                print(diagram_result)
                return diagram_result

        # Umsatz/Liniendiagramm-Fragen direkt an FinanceTool weiterleiten
        if any(w in lower_query for w in ["umsatz", "revenue", "liniendiagramm", "diagramm"]):
            print("📊 Umsatz/Diagramm erkannt – leite an FinanceAnalysisTool weiter.")
            result = Runner.run(self.finance, input_items)
            answer = getattr(result, 'text', None) or getattr(result, 'output', None)
            sources = getattr(result, 'sources', None) if hasattr(result, 'sources') else None
            qa_feedback = qa_ethics_agent.run(answer, sources)
            print("\n---\nQA/Ethik-Check:")
            print(qa_feedback)
            if answer and any(
                phrase in answer.lower() for phrase in [
                    "not_found_year", "nicht gefunden", "keine daten", "nicht verfügbar", "nicht enthalten", "no data", "no financial data", "no revenue", "no net income", "no financials", "no information", "not available", "nan", "bitte stelle eine frage", "keine antwort erhalten"
                ]
            ):
                print("🔍 Unzureichende/fehlende Daten – leite an Websuche weiter.")
                web_result = Runner.run(self.fallback, input_items)
                web_answer = getattr(web_result, 'text', None) or getattr(web_result, 'output', None)
                print("\n---\nWebsuche-Antwort (Fallback):")
                print(web_answer)
                if web_answer and re.search(r"20\d{2}[^\d]*\d+[\.,]?\d*[^\d]*(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", web_answer, re.IGNORECASE):
                    self.last_web_answer = web_answer  # Merken!
                return web_result
            if not answer or answer.strip().lower() in ["quelle: yahoo finance (yfinance)", ""]:
                print("🔍 Leere oder nur Quellenangabe – leite an Websuche weiter.")
                web_result = Runner.run(self.fallback, input_items)
                web_answer = getattr(web_result, 'text', None) or getattr(web_result, 'output', None)
                print("\n---\nWebsuche-Antwort (Fallback):")
                print(web_answer)
                if web_answer and re.search(r"20\d{2}[^\d]*\d+[\.,]?\d*[^\d]*(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", web_answer, re.IGNORECASE):
                    self.last_web_answer = web_answer  # Merken!
                return web_result
            return result

        # Kursanalyse direkt an FinanceTool
        if any(w in lower_query for w in ["prognose", "analyse", "kurs", "aktienentwicklung"]):
            print("📊 Analyse erkannt – leite an FinanceAnalysisTool weiter.")
            result = Runner.run(self.finance, input_items)
            answer = getattr(result, 'text', None) or getattr(result, 'output', None)
            sources = getattr(result, 'sources', None) if hasattr(result, 'sources') else None
            qa_feedback = qa_ethics_agent.run(answer, sources)
            print("\n---\nQA/Ethik-Check:")
            print(qa_feedback)
            if answer and any(
                phrase in answer.lower() for phrase in [
                    "not_found_year", "nicht gefunden", "keine daten", "nicht verfügbar", "nicht enthalten", "no data", "no financial data", "no revenue", "no net income", "no financials", "no information", "not available", "nan", "bitte stelle eine frage", "keine antwort erhalten"
                ]
            ):
                print("🔍 Unzureichende/fehlende Daten – leite an Websuche weiter.")
                web_result = Runner.run(self.fallback, input_items)
                web_answer = getattr(web_result, 'text', None) or getattr(web_result, 'output', None)
                print("\n---\nWebsuche-Antwort (Fallback):")
                print(web_answer)
                if web_answer and re.search(r"20\d{2}[^\d]*\d+[\.,]?\d*[^\d]*(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", web_answer, re.IGNORECASE):
                    self.last_web_answer = web_answer  # Merken!
                return web_result
            if not answer or answer.strip().lower() in ["quelle: yahoo finance (yfinance)", ""]:
                print("🔍 Leere oder nur Quellenangabe – leite an Websuche weiter.")
                web_result = Runner.run(self.fallback, input_items)
                web_answer = getattr(web_result, 'text', None) or getattr(web_result, 'output', None)
                print("\n---\nWebsuche-Antwort (Fallback):")
                print(web_answer)
                if web_answer and re.search(r"20\d{2}[^\d]*\d+[\.,]?\d*[^\d]*(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", web_answer, re.IGNORECASE):
                    self.last_web_answer = web_answer  # Merken!
                return web_result
            return result

        print("🧠 Frage wird zuerst an RAG übergeben...")
        result = Runner.run(self.primary, input_items)

        for item in result.new_items:
            if isinstance(item, MessageOutputItem):
                text = item.text.lower()
                if any(phrase in text for phrase in [
                    "nicht beantworten", "keine daten", "nicht enthalten",
                    "nicht bekannt", "nicht verfügbar", "sorry"
                ]):
                    print("⚠️ Unzureichende Antwort erkannt – Websuche wird aktiviert.")
                    web_result = Runner.run(self.fallback, input_items)
                    web_answer = getattr(web_result, 'text', None) or getattr(web_result, 'output', None)
                    self.last_web_answer = web_answer  # Merken!
                    return web_result

        answer = None
        for item in getattr(result, "new_items", []):
            if hasattr(item, "text") and isinstance(item.text, str) and item.text.strip():
                answer = item.text
                break
        if not answer:
            answer = getattr(result, 'text', None) or getattr(result, 'output', None)
        sources = getattr(result, 'sources', None) if hasattr(result, 'sources') else None
        qa_feedback = qa_ethics_agent.run(answer, sources)
        print("\n---\nQA/Ethik-Check:")
        print(qa_feedback)
        return result

supervisor_agent = SupervisorAgentWithFallback()
