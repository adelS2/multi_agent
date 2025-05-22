# 
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import RetrievalQA
# from dotenv import load_dotenv
# import os
# from web_search_agent import suche_im_web
# #  API-Key setzen
# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# 
# def lade_vektor_db(pfad="chroma_langchain_db"):
#     embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
#     vektor_db = Chroma(persist_directory=pfad, embedding_function=embeddings)
#     return vektor_db
# 
# def starte_rag_system():
#     db = lade_vektor_db()
#     retriever = db.as_retriever()
# 
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash",
#         temperature=0.3
#     )
# 
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         return_source_documents=True  # wichtig, sonst Fehler bei .invoke(...)
#     )
#     return qa_chain
# 
# if __name__ == "__main__":
#     qa = starte_rag_system()
#     frage = input("Frage stellen: ")
#     antwort = qa.invoke({"query": frage})
# 
#     print("\nAntwort:", antwort["result"])
# 
#     for i, doc in enumerate(antwort["source_documents"]):
#         print(f"\n🔎 Quelle {i+1}:")
#         print(doc.metadata)
#         print(doc.page_content[:300], "...")
# if __name__ == "__main__":
#     qa = starte_rag_system()
#     frage = input("Frage stellen: ")
#     antwort = qa.run(frage)
#     
#     if not antwort or "Ich weiß es nicht" in antwort:
#         print("Keine Antwort gefunden. Websuche wird gestartet...")
#         ergebnisse = suche_im_web(frage)
#         for eintrag in ergebnisse:
#             print(f"\nTitel: {eintrag['Titel']}\nLink: {eintrag['Link']}\nBeschreibung: {eintrag['Beschreibung']}")
#     else:
#         print("Antwort:", antwort)
        
        
        
        
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import RetrievalQA
# from dotenv import load_dotenv
# import os
# from web_search_agent import suche_im_web

# # .env laden
# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# def lade_vektor_db(pfad="chroma_langchain_db"):
#     embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
#     vektor_db = Chroma(persist_directory=pfad, embedding_function=embeddings)
#     return vektor_db

# def starte_rag_system():
#     db = lade_vektor_db()
#     retriever = db.as_retriever()

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash",
#         temperature=0.3
#     )

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         return_source_documents=True
#     )
#     return qa_chain

#     # return any(phrase in text for phrase in schlüsselwörter)
# def ist_antwort_unzureichend(text):
#     if not text or len(text.strip()) < 30:
#         return True
#     text = text.lower()
#     schlüsselwörter = [
#         "ich kann", "nicht nennen", "keine echtzeit", "nicht verfügbar",
#         "nicht zur verfügung", "nicht bekannt", "bedauerlicherweise", "kann ich nicht",
#         "keine information", "unbekannt", "leider", "nicht sicher", "nicht möglich",
#         "nicht enthalten", "nicht gefunden", "nur zu apple", "enthält keine daten",
#         "die dokumente betreffen apple"
#     ]
#     return any(phrase in text for phrase in schlüsselwörter)

# if __name__ == "__main__":
#     qa = starte_rag_system()
#     frage = input("Frage stellen: ")

#     antwort = qa.invoke({"query": frage})
#     antwort_text = antwort.get("result", "")
#     quellen = antwort.get("source_documents", [])

#     print("\n🧠 Antwort des RAG-Systems:")
#     print(antwort_text)

#     # Bedingung für unzureichende Antwort oder zu wenige Quellen
#     if ist_antwort_unzureichend(antwort_text) or len(quellen) < 2:
#         print("\n⚠️ Antwort war unzureichend oder basiert auf zu wenigen Quellen.")
#         print("🌐 Starte stattdessen eine Websuche...\n")
#         ergebnisse = suche_im_web(frage)
#         for eintrag in ergebnisse:
#             print(f"\n🌐 Titel: {eintrag['Titel']}\n🔗 Link: {eintrag['Link']}\n📄 Beschreibung: {eintrag['Beschreibung']}")
#     else:
#         print("\n📚 Quellen aus Vektor-Datenbank:")
#         for i, doc in enumerate(quellen):
#             print(f"\n🔎 Quelle {i+1}:")
#             print(doc.metadata)
#             print(doc.page_content[:300], "...")
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# === .env laden ===
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# === Vektor-Datenbank vorbereiten ===
def lade_vektor_db(pfad="chroma_langchain_db"):
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    vektor_db = Chroma(persist_directory=pfad, embedding_function=embeddings)
    return vektor_db

# === RAG-System initialisieren ===
def starte_rag_system():
    db = lade_vektor_db()
    retriever = db.as_retriever()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

# === Antwortqualität prüfen ===
def ist_antwort_unzureichend(text):
    if not text or len(text.strip()) < 30:
        return True
    text = text.lower()
    schlüsselwörter = [
        "ich kann", "nicht nennen", "keine echtzeit", "nicht verfügbar",
        "nicht zur verfügung", "nicht bekannt", "bedauerlicherweise", "kann ich nicht",
        "keine information", "unbekannt", "leider", "nicht sicher", "nicht möglich",
        "nicht enthalten", "nicht gefunden"
    ]
    return any(phrase in text for phrase in schlüsselwörter)

if __name__ == "__main__":
    qa = starte_rag_system()
    frage = input("Frage stellen: ")
    antwort = qa.invoke({"query": frage})
    print("\n🧠 Antwort des RAG-Systems:")
    print(antwort["result"])
    quellen = antwort.get("source_documents", [])
    if quellen:
        print("\n📚 Quellen aus Chroma-Vektor-Datenbank:")
        for i, doc in enumerate(quellen):
            print(f"\n🔎 Quelle {i+1}:")
            print(doc.metadata)
            print(doc.page_content[:300], "...")
    else:
        print("\n⚠️ Keine Quellen aus der Vektor-Datenbank gefunden!")
