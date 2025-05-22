from main_rag import starte_rag_system

class RAGSearchTool:
    name = "RAGSearchTool"
    description = "Durchsucht die Vektor-Datenbank nach bekannten Fakten."

    def __call__(self, query: str):
        qa = starte_rag_system()
        antwort = qa.invoke({"query": query})
        return antwort.get("result", "Keine RAG-Antwort gefunden.")
