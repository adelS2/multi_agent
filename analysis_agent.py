# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns

# def lade_neuste_csv():
#     dateien = [f for f in os.listdir() if f.startswith("web_suche_ergebnisse_") and f.endswith(".csv")]
#     if not dateien:
#         print("Keine CSV-Dateien gefunden.")
#         return None
#     dateien.sort(reverse=True)
#     return dateien[0]

# def analysiere_finanzbegriffe(csv_datei):
#     df = pd.read_csv(csv_datei)

#     finanz_keywords = ["Aktie", "Börse", "Kurs", "Gewinn", "Verlust", "Umsatz", "Dividende", "Invest", "Inflation"]
#     df["Relevanz"] = df["Beschreibung"].apply(
#         lambda x: any(kw.lower() in str(x).lower() for kw in finanz_keywords)
#     )

#     relevante = df[df["Relevanz"]]
#     print(f"{len(relevante)} relevante Einträge gefunden.")

#     for index, row in relevante.iterrows():
#         print("\n📌 Titel:", row["Titel"])
#         print("🔗 Link:", row["Link"])
#         print("📝 Beschreibung:", row["Beschreibung"])

#     return relevante

# def visualisiere_treffer(relevante_df):
#     if relevante_df.empty:
#         print("Keine Daten für Visualisierung.")
#         return
#     plt.figure(figsize=(10, 4))
#     sns.countplot(y=relevante_df["Titel"], palette="Blues_d")
#     plt.title("Relevante Finanzthemen aus Web-Suche")
#     plt.xlabel("Häufigkeit")
#     plt.tight_layout()
#     plt.show()

# if __name__ == "__main__":
#     datei = lade_neuste_csv()
#     if datei:
#         relevante = analysiere_finanzbegriffe(datei)
#         visualisiere_treffer(relevante)
# import yfinance as yf
# import matplotlib.pyplot as plt
# import pandas as pd
# from prophet import Prophet
# import uuid
# import os

# from tool_base import ToolBase

# class FinanceAnalysisTool(ToolBase):
#     name = "FinanceAnalysisTool"
#     description = "Führt historische Kursanalysen und Prognosen für Aktienunternehmen durch."

#     async def invoke(self, input_text: str) -> str:
#         # Beispiel: "Analysieren Sie Microsofts Aktienentwicklung im letzten Jahr und prognostizieren Sie das nächste Quartal."
#         if "microsoft" in input_text.lower():
#             ticker = "MSFT"
#         elif "apple" in input_text.lower():
#             ticker = "AAPL"
#         elif "meta" in input_text.lower():
#             ticker = "META"
#         else:
#             return "⚠️ Kein unterstützter Firmenname erkannt für Prognose."

#         try:
#             df = yf.download(ticker, period="1y")
#             df = df.reset_index()
#             df = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

#             model = Prophet()
#             model.fit(df)
#             future = model.make_future_dataframe(periods=90)
#             forecast = model.predict(future)

#             fig = model.plot(forecast)
#             plot_path = f"forecast_{uuid.uuid4().hex}.png"
#             fig.savefig(plot_path)

#             letzte = forecast.tail(1).iloc[0]
#             wert = letzte['yhat']
#             datum = letzte['ds'].strftime('%d.%m.%Y')

#             antwort = (
#                 f"📈 Prognose: Der vorhergesagte Kurs für {ticker} am {datum} liegt bei etwa {wert:.2f} USD.\n"
#                 f"Das zugehörige Prognose-Diagramm wurde erstellt und gespeichert unter: {plot_path}"
#             )
#             return antwort

#         except Exception as e:
#             return f"❌ Fehler bei Analyse: {e}"


import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
import uuid
import os
import asyncio

from tool_base import ToolBase

class FinanceAnalysisTool(ToolBase):
    name = "FinanceAnalysisTool"
    description = "Führt historische Kursanalysen und Prognosen für Aktienunternehmen durch."

    async def invoke(self, input_text: str) -> str:
        if "microsoft" in input_text.lower():
            ticker = "MSFT"
        elif "apple" in input_text.lower():
            ticker = "AAPL"
        elif "meta" in input_text.lower():
            ticker = "META"
        else:
            return "⚠️ Kein unterstützter Firmenname erkannt für Prognose."

        try:
            df = yf.download(ticker, period="1y")
            df = df.reset_index()
            df = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

            # Robuste Datenprüfung
            if df.empty or df['y'].isnull().all():
                return "⚠️ Keine gültigen Kursdaten für die Prognose verfügbar."

            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=90)
            forecast = model.predict(future)

            if forecast.empty or "yhat" not in forecast.columns:
                return "⚠️ Keine gültige Prognose erzeugt."

            fig = model.plot(forecast)
            plot_path = f"forecast_{uuid.uuid4().hex}.png"
            fig.savefig(plot_path)

            letzte = forecast.iloc[-1]
            wert = letzte['yhat']
            datum = letzte['ds'].strftime('%d.%m.%Y')

            antwort = (
                f"📈 Prognose: Der vorhergesagte Kurs für {ticker} am {datum} liegt bei etwa {wert:.2f} USD.\n"
                f"Das zugehörige Prognose-Diagramm wurde erstellt und gespeichert unter: {plot_path}"
            )
            return antwort

        except Exception as e:
            return f"❌ Fehler bei Analyse: {e}"

    # ✅ __call__-Fix für Runner
    def __call__(self, input_text: str) -> str:
        return asyncio.run(self.invoke(input_text))
