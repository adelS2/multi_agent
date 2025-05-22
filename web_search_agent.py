# # from serpapi import GoogleSearch
# # from dotenv import load_dotenv
# # import pandas as pd
# # import datetime
# # import os

# # # .env-Datei laden
# # load_dotenv()

# # # API-Key aus Umgebungsvariablen lesen
# # api_key = os.getenv("SERPAPI_API_KEY")
# # # GoogleSearch-Objekt erstellen

# # def suche_im_web(frage, anzahl=5):
# #     params = {
# #         "engine": "google_finance",
# #         "q": frage,
# #         "num": anzahl,
# #         "hl": "de",
# #     }

# #     search = GoogleSearch(params)
# #     ergebnisse = search.get_dict()

# #     resultate = []

# #     for eintrag in ergebnisse.get("organic_results", []):
# #         resultate.append({
# #             "Titel": eintrag.get("title"),
# #             "Link": eintrag.get("link"),
# #             "Beschreibung": eintrag.get("snippet")
# #         })

# #     # Speichern in CSV
# #     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# #     dateiname = f"web_suche_ergebnisse_{timestamp}.csv"
# #     df = pd.DataFrame(resultate)
# #     df.to_csv(dateiname, index=False, encoding="utf-8")
# #     print(f"Web-Suchergebnisse gespeichert in: {dateiname}")

# #     return resultate
# # from serpapi import GoogleSearch
# # from dotenv import load_dotenv
# # import pandas as pd
# # import datetime
# # import os

# # # .env laden
# # load_dotenv()

# # # API-Key laden
# # api_key = os.getenv("SERPAPI_API_KEY")

# # def suche_im_web(frage, anzahl=5):
# #     params = {
# #         "engine": "google",  
# #         "q": frage,
# #         "num": anzahl,
# #         "hl": "de",
# #         "api_key": api_key
# #     }

# #     try:
# #         search = GoogleSearch(params)
# #         ergebnisse = search.get_dict()
# #     except Exception as e:
# #         print(f"❌ Fehler bei der Websuche: {e}")
# #         return []

# #     resultate = []
# #     for eintrag in ergebnisse.get("organic_results", []):
# #         resultate.append({
# #             "Titel": eintrag.get("title"),
# #             "Link": eintrag.get("link"),
# #             "Beschreibung": eintrag.get("snippet")
# #         })

# #     # Speichern in CSV
# #     if resultate:
# #         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# #         dateiname = f"web_suche_ergebnisse_{timestamp}.csv"
# #         pd.DataFrame(resultate).to_csv(dateiname, index=False, encoding="utf-8")
# #         print(f"\n💾 Web-Suchergebnisse gespeichert in: {dateiname}")

# #     return resultate




# #import requests
# #import yfinance as yf
# #from datetime import datetime, timedelta
# #import os
# #from dotenv import load_dotenv
# ## === Konfiguration ===
# #load_dotenv()
# ## API-Keys und URLs
# #NEWS_API_URL = "https://newsapi.org/v2/everything"
# #NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# #def hole_aktienkurs(ticker):
# #    aktie = yf.Ticker(ticker)
# #    # hole den Kurs vom heutigen Tag (Close)
# #    heute = datetime.now().date()
# #    start = heute - timedelta(days=2)
# #    df = aktie.history(start=start, end=heute + timedelta(days=1))
# #    if not df.empty:
# #        letzter_kurs = df['Close'][-1]
# #        vorheriger_kurs = df['Close'][-2]
# #        prozent = ((letzter_kurs - vorheriger_kurs) / vorheriger_kurs) * 100
# #        return letzter_kurs, prozent
# #    return None, None
# #
# #def hole_nachrichten(ticker, anzahl=5):
# #    heute = datetime.now().date()
# #    start_datum = heute - timedelta(days=1)
# #    
# #    params = {
# #        "q": ticker,
# #        "from": start_datum.isoformat(),
# #        "language": "de",
# #        "sortBy": "relevancy",
# #        "pageSize": anzahl,
# #        "apiKey": NEWS_API_KEY
# #    }
# #    
# #    antwort = requests.get(NEWS_API_URL, params=params)
# #    daten = antwort.json()
# #    
# #    nachrichten = []
# #    if daten.get("status") == "ok":
# #        for artikel in daten.get("articles", []):
# #            nachrichten.append({
# #                "titel": artikel["title"],
# #                "beschreibung": artikel["description"],
# #                "quelle": artikel["source"]["name"],
# #                "datum": artikel["publishedAt"]
# #            })
# #    return nachrichten
# #
# #def erstelle_zusammenfassung(ticker, kurs, prozent, nachrichten):
# #    if kurs is None or prozent is None:
# #        return "Keine aktuellen Kursdaten verfügbar."
# #    
# #    richtung = "gestiegen" if prozent > 0 else "gefallen"
# #    prozent_text = f"{abs(prozent):.2f} %"
# #    
# #    if nachrichten:
# #        # Die wichtigste Nachricht (erste) nutzen
# #        wichtigste = nachrichten[0]
# #        text = (
# #            f"{ticker}-Aktie ist heute um {prozent_text} {richtung}, "
# #            f"ausgelöst durch folgende Nachricht: „{wichtigste['titel']}“ "
# #            f"(Quelle: {wichtigste['quelle']}, {wichtigste['datum'][:10]})."
# #        )
# #    else:
# #        text = f"{ticker}-Aktie ist heute um {prozent_text} {richtung}, aber es gibt keine aktuellen Nachrichten."
# #    return text
# #
# #if __name__ == "__main__":
# #    aktie = "GOOG"
# #    
# #    kurs, prozent = hole_aktienkurs(aktie)
# #    nachrichten = hole_nachrichten(aktie, anzahl=3)
# #    
# #    zusammenfassung = erstelle_zusammenfassung(aktie, kurs, prozent, nachrichten)
# #    print(zusammenfassung)

# # import os
# # import datetime
# # import pandas as pd
# # import yfinance as yf
# # from dotenv import load_dotenv
# # from serpapi import GoogleSearch

# # # === Konfiguration ===
# # load_dotenv()
# # SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

# # # === 1. Firma und Ticker automatisch erkennen ===
# # def erkenne_firma_und_ticker(frage):
# #     """
# #     Nutzt Mapping, um Firma und Börsenticker aus einer Frage zu extrahieren.
# #     """
# #     mapping = {
# #         "apple": "AAPL",
# #         "microsoft": "MSFT",
# #         "google": "GOOG",
# #         "alphabet": "GOOG",
# #         "meta": "META",
# #         "facebook": "META",
# #         "amazon": "AMZN",
# #         "tesla": "TSLA",
# #         "nvidia": "NVDA",
# #         "aramco": "2222.SR"
# #     }

# #     frage_lc = frage.lower()
# #     for name, ticker in mapping.items():
# #         if name in frage_lc:
# #             return name.capitalize(), ticker

# #     return None, None

# # # === 2. Kursdaten abrufen ===
# # def hole_aktienkurs(ticker):
# #     aktie = yf.Ticker(ticker)
# #     heute = datetime.datetime.now().date()
# #     start = heute - datetime.timedelta(days=2)
# #     df = aktie.history(start=start, end=heute + datetime.timedelta(days=1))

# #     if df.empty or len(df) < 2:
# #         return None, None

# #     letzter_kurs = df['Close'].iloc[-1]
# #     vorheriger_kurs = df['Close'].iloc[-2]
# #     prozent = ((letzter_kurs - vorheriger_kurs) / vorheriger_kurs) * 100
# #     return round(letzter_kurs, 2), round(prozent, 2)

# # # === 3. Nachrichten suchen ===
# # def hole_nachrichten(firma, anzahl=5):
# #     params = {
# #         "engine": "google",
# #         "q": f"{firma} aktiennachrichten",
# #         "num": anzahl,
# #         "hl": "de",
# #         "api_key": SERPAPI_KEY
# #     }

# #     try:
# #         search = GoogleSearch(params)
# #         ergebnisse = search.get_dict()
# #     except Exception as e:
# #         print(f"❌ Fehler bei der Websuche: {e}")
# #         return []

# #     resultate = []
# #     for eintrag in ergebnisse.get("organic_results", []):
# #         resultate.append({
# #             "Titel": eintrag.get("title"),
# #             "Link": eintrag.get("link"),
# #             "Beschreibung": eintrag.get("snippet")
# #         })

# #     if resultate:
# #         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# #         dateiname = f"web_suche_ergebnisse_{timestamp}.csv"
# #         pd.DataFrame(resultate).to_csv(dateiname, index=False, encoding="utf-8")
# #         print(f"\n💾 Web-Suchergebnisse gespeichert in: {dateiname}")

# #     return resultate

# # # === 4. Zusammenfassung generieren ===
# # def erstelle_zusammenfassung(firma, ticker):
# #     kurs, prozent = hole_aktienkurs(ticker)
# #     nachrichten = hole_nachrichten(firma)

# #     heute = datetime.datetime.now().strftime("%d. %B %Y")
# #     richtung = "gestiegen" if prozent and prozent > 0 else "gefallen"
# #     prozent_text = f"{abs(prozent):.2f} %" if prozent is not None else "unbekannt"

# #     if nachrichten:
# #         wichtigste = nachrichten[0]
# #         quelle = wichtigste["Link"]
# #         beschreibung = wichtigste["Beschreibung"]
# #         zusammenfassung = (
# #             f"{firma}s Aktie ist heute um {prozent_text} {richtung}, "
# #             f"ausgelöst durch folgende Nachricht: „{beschreibung}“ "
# #             f"(Quelle: {quelle}, {heute})."
# #         )
# #     else:
# #         zusammenfassung = (
# #             f"{firma}s Aktie ist heute um {prozent_text} {richtung}, "
# #             f"aber es liegen keine aktuellen Nachrichten vor."
# #         )

# #     print("\n🧾 Zusammenfassung:")
# #     print(zusammenfassung)
# #     return zusammenfassung

# # # === 5. Testnutzung für Standalone ===
# # if __name__ == "__main__":
# #     frage = input("❓ Frage eingeben: ").strip()
# #     firma, ticker = erkenne_firma_und_ticker(frage)

# #     if not firma or not ticker:
# #         print("❌ Keine bekannte Firma in der Frage erkannt.")
# #     else:
# #         erstelle_zusammenfassung(firma, ticker)


# import os
# import datetime
# import pandas as pd
# import yfinance as yf
# from dotenv import load_dotenv
# from serpapi import GoogleSearch

# # === Konfiguration ===
# load_dotenv()
# SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

# # === 1. Firma aus Frage erkennen
# def erkenne_firma_aus_frage(frage):
#     frage_lc = frage.lower()
#     kandidaten = [
#         "apple", "microsoft", "google", "alphabet", "meta", "facebook",
#         "amazon", "tesla", "nvidia", "aramco", "samsung", "bmw", "siemens",
#         "sap", "netflix", "intel", "adidas", "deutsche bank", "asus", "logetic", "sixt"
#     ]
#     for name in kandidaten:
#         if name in frage_lc:
#             return name.capitalize()
#     worte = frage_lc.split()
#     for wort in reversed(worte):
#         if wort.isalpha() and len(wort) > 2:
#             return wort.capitalize()
#     return None

# # === 2. Ticker-Suche über Web + Filter
# def finde_ticker_via_websuche(firma):
#     print(f"🔎 Versuche, Ticker für '{firma}' zu finden...")
#     params = {
#         "engine": "google",
#         "q": f"{firma} aktien ticker",
#         "hl": "de",
#         "api_key": SERPAPI_KEY,
#         "num": 5
#     }
#     verbotene_woerter = {"AKTIE", "AKTIEN", "DER", "NEWS", "BÖRSE", "UND"}

#     try:
#         search = GoogleSearch(params)
#         results = search.get_dict().get("organic_results", [])
#         for eintrag in results:
#             snippet = (eintrag.get("snippet") or "").upper()
#             for wort in snippet.split():
#                 if (
#                     wort.isalnum()
#                     and 3 <= len(wort) <= 6
#                     and wort.isupper()
#                     and wort not in verbotene_woerter
#                 ):
#                     print(f"✅ Möglicher Ticker gefunden: {wort}")
#                     return wort
#     except Exception as e:
#         print(f"❌ Fehler bei Ticker-Suche: {e}")
#     print(f"⚠️ Kein Ticker für '{firma}' gefunden.")
#     return None

# # === 3. Gültigkeit des Tickers prüfen
# def ist_gueltiger_ticker(ticker):
#     try:
#         aktie = yf.Ticker(ticker)
#         info = aktie.info
#         return "shortName" in info and info["shortName"]
#     except Exception:
#         return False

# # === 4. Zentrale Funktion: Firma & Ticker ermitteln
# def erkenne_firma_und_ticker(frage):
#     firma = erkenne_firma_aus_frage(frage)
#     if not firma:
#         return None, None

#     # Manuelles Mapping für Spezialfälle
#     if firma.lower() in ["google", "alphabet"]:
#         return "Alphabet", "GOOG"
#     if firma.lower() == "facebook":
#         return "Meta", "META"

#     ticker = finde_ticker_via_websuche(firma)
#     if ticker and ist_gueltiger_ticker(ticker):
#         return firma, ticker

#     print(f"⚠️ Gefundener Ticker '{ticker}' ist ungültig oder liefert keine Daten.")
#     return firma, None

# # === 5. Kursdaten abrufen
# def hole_aktienkurs(ticker):
#     try:
#         aktie = yf.Ticker(ticker)
#         heute = datetime.datetime.now().date()
#         start = heute - datetime.timedelta(days=2)
#         df = aktie.history(start=start, end=heute + datetime.timedelta(days=1))

#         if df.empty or len(df) < 2:
#             return None, None

#         letzter_kurs = df['Close'].iloc[-1]
#         vorheriger_kurs = df['Close'].iloc[-2]
#         prozent = ((letzter_kurs - vorheriger_kurs) / vorheriger_kurs) * 100
#         return round(letzter_kurs, 2), round(prozent, 2)
#     except Exception as e:
#         print(f"❌ Fehler beim Abrufen von Kursdaten für {ticker}: {e}")
#         return None, None

# # === 6. Nachrichten holen
# def hole_nachrichten(firma, anzahl=5):
#     params = {
#         "engine": "google",
#         "q": f"{firma} aktiennachrichten",
#         "num": anzahl,
#         "hl": "de",
#         "api_key": SERPAPI_KEY
#     }
#     try:
#         search = GoogleSearch(params)
#         ergebnisse = search.get_dict()
#     except Exception as e:
#         print(f"❌ Fehler bei der Websuche: {e}")
#         return []

#     resultate = []
#     for eintrag in ergebnisse.get("organic_results", []):
#         resultate.append({
#             "Titel": eintrag.get("title"),
#             "Link": eintrag.get("link"),
#             "Beschreibung": eintrag.get("snippet")
#         })

#     if resultate:
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         dateiname = f"web_suche_ergebnisse_{timestamp}.csv"
#         pd.DataFrame(resultate).to_csv(dateiname, index=False, encoding="utf-8")
#         print(f"\n💾 Web-Suchergebnisse gespeichert in: {dateiname}")

#     return resultate

# # === 7. Zusammenfassung generieren
# def erstelle_zusammenfassung(firma, ticker):
#     kurs, prozent = hole_aktienkurs(ticker)
#     nachrichten = hole_nachrichten(firma)

#     heute = datetime.datetime.now().strftime("%d. %B %Y")
#     richtung = "gestiegen" if prozent and prozent > 0 else "gefallen"
#     prozent_text = f"{abs(prozent):.2f} %" if prozent is not None else "unbekannt"

#     if nachrichten:
#         wichtigste = nachrichten[0]
#         quelle = wichtigste["Link"]
#         beschreibung = wichtigste["Beschreibung"]
#         zusammenfassung = (
#             f"{firma}s Aktie ist heute um {prozent_text} {richtung}, "
#             f"ausgelöst durch folgende Nachricht: „{beschreibung}“ "
#             f"(Quelle: {quelle}, {heute})."
#         )
#     else:
#         zusammenfassung = (
#             f"{firma}s Aktie ist heute um {prozent_text} {richtung}, "
#             f"aber es liegen keine aktuellen Nachrichten vor."
#         )

#     print("\n🧾 Zusammenfassung:")
#     print(zusammenfassung)
#     return zusammenfassung

# # === 8. Manuelle Tests
# if __name__ == "__main__":
#     frage = input("❓ Frage eingeben: ").strip()
#     firma, ticker = erkenne_firma_und_ticker(frage)
#     if not firma:
#         print("❌ Keine Firma erkannt.")
#     elif not ticker:
#         print(f"⚠️ Firma '{firma}' erkannt, aber kein gültiger Ticker gefunden.")
#     else:
#         erstelle_zusammenfassung(firma, ticker)
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import pandas as pd
import datetime

load_dotenv()
api_key = os.getenv("SERPAPI_API_KEY")

def suche_im_web(frage, anzahl=5):
    params = {
        "engine": "google",
        "q": frage,
        "num": anzahl,
        "hl": "de",
        "api_key": api_key
    }

    try:
        search = GoogleSearch(params)
        ergebnisse = search.get_dict()
    except Exception as e:
        return [f"Fehler bei der Websuche: {e}"]

    resultate = []
    for eintrag in ergebnisse.get("organic_results", []):
        resultate.append({
            "Titel": eintrag.get("title"),
            "Link": eintrag.get("link"),
            "Beschreibung": eintrag.get("snippet")
        })

    # Optional: CSV speichern
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pd.DataFrame(resultate).to_csv(f"web_suche_ergebnisse_{timestamp}.csv", index=False)

    return resultate
