from web_search_agent import suche_im_web

class WebSearchTool:
    name = "WebSearchTool"
    description = "Führt eine Google Websuche aus (SerpAPI)."

    def __call__(self, query: str):
        ergebnisse = suche_im_web(query)
        return "\n".join([f"{e['Titel']}: {e['Beschreibung']}" for e in ergebnisse[:3]]) or "Keine Web-Ergebnisse."
