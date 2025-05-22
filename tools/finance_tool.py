import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
import uuid
import os
import asyncio
import sys
import traceback
import numpy as np
import webbrowser
import difflib
import re

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tool_base import ToolBase

class FinanceAnalysisTool(ToolBase):
    name = "FinanceAnalysisTool"
    description = "Führt historische Kursanalysen und Prognosen für Aktienunternehmen durch."

    async def invoke(self, input_text: str) -> str:
        print("✅ GELADEN: finance_tool.py (richtige Version aktiv)")

        # Mapping für gängige Firmennamen zu Ticker
        name2ticker = {
            'microsoft': 'MSFT',
            'apple': 'AAPL',
            'meta': 'META',
            'facebook': 'META',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'nvidia': 'NVDA',
            'netflix': 'NFLX',
            'ibm': 'IBM',
            'intel': 'INTC',
            'adobe': 'ADBE',
            'sap': 'SAP',
            'siemens': 'SIE.DE',
            'bayer': 'BAYN.DE',
            'biontech': 'BNTX',
            'pfizer': 'PFE',
            'bayerische': 'BAYN.DE',
            'deutsche bank': 'DBK.DE',
            'commerzbank': 'CBK.DE',
            'volkswagen': 'VOW3.DE',
            'bmw': 'BMW.DE',
            'mercedes': 'MBG.DE',
            'mercedes-benz': 'MBG.DE',
            'asus': '2357.TW',
            'samsung': '005930.KS',
            'samsung electronics': '005930.KS',
        }
        input_lower = input_text.lower()
        # Firmennamen/Ticker gezielt aus der Frage extrahieren (mit Fuzzy Matching)
        gewuenschte_ticker = []
        for name, ticker in name2ticker.items():
            if name in input_lower or ticker.lower() in input_lower:
                gewuenschte_ticker.append((name, ticker))
        # Fuzzy Matching für Tippfehler
        if not gewuenschte_ticker:
            words = re.findall(r'[a-zA-Z0-9.-]+', input_lower)
            close_names = difflib.get_close_matches(
                ' '.join(words), list(name2ticker.keys()), n=1, cutoff=0.8)
            if close_names:
                name = close_names[0]
                gewuenschte_ticker.append((name, name2ticker[name]))
        # Falls kein bekannter Name gefunden, prüfe auf expliziten Ticker im Text
        if not gewuenschte_ticker:
            tokens = re.split(r'[^a-zA-Z0-9.-]+', input_text.strip())
            for token in tokens:
                t = token.strip().upper()
                if t in name2ticker.values():
                    gewuenschte_ticker.append((t, t))
        # Duplikate entfernen: Nur ein Eintrag pro Ticker
        unique_ticker = {}
        for name, ticker in gewuenschte_ticker:
            unique_ticker[ticker] = name  # Überschreibt ggf. vorherige, aber das ist ok
        gewuenschte_ticker = [(name, ticker) for ticker, name in unique_ticker.items()]
        if not gewuenschte_ticker:
            return "⚠️ Kein unterstützter Firmenname oder Ticker erkannt. Beispiele: Microsoft, GOOGL, SAP.DE, ..."
        # Jahr extrahieren (z.B. 2023)
        jahr_match = re.search(r'(20\d{2})', input_lower)
        jahr_gewünscht = jahr_match.group(1) if jahr_match else None
        # Prüfe, ob die Frage nach Prognose/Diagramm/Chart fragt
        prognose_keywords = ["prognose", "vorhersage", "forecast", "diagramm", "chart", "visualisierung", "plot"]
        will_prognose = any(kw in input_lower for kw in prognose_keywords)

        antworten = []
        if will_prognose:
            for name, ticker in gewuenschte_ticker:
                try:
                    print(f"Starte Prognose für {name} ({ticker}) ...")
                    df = yf.download(ticker, period="1y")
                    df = df.reset_index()

                    # Zeitspalte finden
                    zeit_spalte = None
                    for candidate in ['Date', 'Datetime', 'index']:
                        if candidate in df.columns:
                            zeit_spalte = candidate
                            break
                    if zeit_spalte is None:
                        zeit_spalte = df.columns[0]  # Fallback: erste Spalte

                    # Kurs-Spalte finden
                    kurs_spalte = None
                    if 'Close' in df.columns:
                        kurs_spalte = 'Close'
                    elif ticker in df.columns:
                        kurs_spalte = ticker
                    else:
                        float_cols = df.select_dtypes(include='float').columns
                        if len(float_cols) > 0:
                            kurs_spalte = float_cols[0]
                        else:
                            antworten.append("⚠️ Keine gültigen Kursdaten gefunden.")
                            continue

                    df = df[[zeit_spalte, kurs_spalte]].rename(columns={zeit_spalte: 'ds', kurs_spalte: 'y'})
                    # Erzwinge 1D-Series für Prophet (maximal robust)
                    y_raw = df['y']
                    if isinstance(y_raw, pd.DataFrame):
                        y_raw = y_raw.squeeze(axis=1)
                    arr = np.asarray(y_raw).flatten()
                    if len(df) != len(arr):
                        print(f'WARNUNG: Index und Kursreihe unterschiedlich lang! df: {len(df)}, arr: {len(arr)}')
                        df = df.iloc[:len(arr)]
                    if not df.index.is_unique or len(df.index) != len(arr):
                        print('WARNUNG: Index nicht eindeutig oder nicht passend, setze RangeIndex!')
                        df.index = pd.RangeIndex(len(arr))
                    # Spalte y löschen, dann als Series neu zuweisen
                    if 'y' in df:
                        del df['y']
                    df['y'] = pd.Series(arr, index=df.index)
                    print("DEBUG: type(df['y']) =", type(df['y']), "shape =", getattr(df['y'], 'shape', None))
                    df['y'] = pd.to_numeric(df['y'], errors='coerce')
                    print(f'df["y"] nach Umwandlung: type={type(df["y"])} shape={getattr(df["y"], "shape", None)}')

                    if df.empty or pd.Series(df['y']).isnull().values.all():
                        print("✅ .all() wurde wirklich ausgeführt")
                        antworten.append("⚠️ Keine gültigen Kursdaten für die Prognose verfügbar.")
                        continue

                    model = Prophet()
                    model.fit(df)
                    future = model.make_future_dataframe(periods=90)
                    forecast = model.predict(future)

                    if forecast.empty or "yhat" not in forecast.columns or forecast["yhat"].isnull().all():
                        antworten.append("⚠️ Keine gültige Prognose erzeugt – yhat fehlt oder ist leer.")
                        continue

                    letzte = forecast.iloc[-1]
                    wert = letzte["yhat"]
                    datum = letzte["ds"]
                    if hasattr(datum, 'strftime'):
                        datum = datum.strftime("%d.%m.%Y")

                    fig = model.plot(forecast)
                    plot_path = f"forecast_{uuid.uuid4().hex}.png"
                    fig.savefig(plot_path)
                    webbrowser.open(plot_path)

                    antwort = (
                        f"📈 Prognose: Der vorhergesagte Kurs für {ticker} am {datum} liegt bei etwa {wert:.2f} USD.\n"
                        f"Das zugehörige Prognose-Diagramm wurde erstellt und gespeichert unter: {plot_path}\n"
                        f"Quelle: Yahoo Finance (yfinance)"
                    )
                    antworten.append(antwort)

                except Exception as e:
                    antworten.append(f"❌ Fehler bei Analyse für {name} ({ticker}): {e}\nQuelle: Yahoo Finance (yfinance)")
        # Umsatz-Liniendiagramm und Umsatzdaten nur, wenn nach Umsatz gefragt wird
        elif 'umsatz' in input_lower:
            umsatz_antworten = []
            for name, ticker in gewuenschte_ticker:
                try:
                    stock = yf.Ticker(ticker)
                    fin = stock.financials
                    if fin is not None and not fin.empty and 'Total Revenue' in fin.index:
                        revenue = fin.loc['Total Revenue']
                        revenue = revenue.sort_index()
                        years = [str(d.year) for d in revenue.index]
                        values = revenue.values / 1e9  # in Mrd. USD
                        if jahr_gewünscht and jahr_gewünscht in years:
                            idx = years.index(jahr_gewünscht)
                            umsatz_text = f"Umsatz von {ticker} im Jahr {jahr_gewünscht}: {values[idx]:.2f} Mrd. USD\nQuelle: Yahoo Finance (yfinance)"
                        else:
                            umsatz_text = ", ".join([f"{jahr}: {val:.2f} Mrd. USD" for jahr, val in zip(years, values)]) + "\nQuelle: Yahoo Finance (yfinance)"
                        umsatz_antworten.append(umsatz_text)
                        continue
                    fin = stock.quarterly_financials
                    if fin is not None and not fin.empty and 'Total Revenue' in fin.index:
                        revenue = fin.loc['Total Revenue']
                        revenue = revenue.sort_index()
                        labels = [d.strftime('%Y-%m') for d in revenue.index]
                        values = revenue.values / 1e9
                        umsatz_text = ", ".join([f"{label}: {val:.2f} Mrd. USD" for label, val in zip(labels, values)])
                        umsatz_antworten.append(f"Umsatz von {ticker} in den letzten Quartalen: {umsatz_text}\nQuelle: Yahoo Finance (yfinance)")
                        continue
                    umsatz_antworten.append(f'⚠️ Umsatzdaten für {ticker} konnten nicht gefunden werden.\nQuelle: Yahoo Finance (yfinance)')
                except Exception as e:
                    umsatz_antworten.append(f'❌ Fehler beim Abrufen der Umsatzdaten für {ticker}: {e}\nQuelle: Yahoo Finance (yfinance)')
            return "\n\n".join(umsatz_antworten)
        # Umsatz-Vergleichsdiagramm für mehrere Jahre, falls Bereich erkannt
        umsatz_bereich = re.search(r'(20\d{2})\s*(?:bis|-|–|—|to)\s*(20\d{2})', input_lower)
        umsatz_bereich_start = umsatz_bereich.group(1) if umsatz_bereich else None
        umsatz_bereich_ende = umsatz_bereich.group(2) if umsatz_bereich else None
        if 'umsatz' in input_lower and umsatz_bereich_start and umsatz_bereich_ende:
            umsatz_antworten = []
            for name, ticker in gewuenschte_ticker:
                try:
                    stock = yf.Ticker(ticker)
                    fin = stock.financials
                    if fin is not None and not fin.empty and 'Total Revenue' in fin.index:
                        revenue = fin.loc['Total Revenue']
                        revenue = revenue.sort_index()
                        years = [str(d.year) for d in revenue.index]
                        values = revenue.values / 1e9  # in Mrd. USD
                        # Filter für gewünschten Bereich
                        jahr_start = int(umsatz_bereich_start)
                        jahr_ende = int(umsatz_bereich_ende)
                        years_filtered = []
                        values_filtered = []
                        for jahr, val in zip(years, values):
                            if jahr_start <= int(jahr) <= jahr_ende:
                                years_filtered.append(jahr)
                                values_filtered.append(val)
                        if years_filtered:
                            plt.figure(figsize=(8,4))
                            plt.bar(years_filtered, values_filtered, color='royalblue')
                            plt.title(f'Umsatz von {ticker} ({jahr_start}-{jahr_ende})')
                            plt.xlabel('Jahr')
                            plt.ylabel('Umsatz (Mrd. USD)')
                            plt.grid(axis='y')
                            fname = f'{ticker}_umsatz_vergleich_{jahr_start}_{jahr_ende}_{uuid.uuid4().hex}.png'
                            plt.savefig(fname)
                            plt.close()
                            umsatz_antworten.append(f'📊 Umsatz-Vergleichsdiagramm für {ticker} ({jahr_start}-{jahr_ende}) gespeichert unter: {fname}\nQuelle: Yahoo Finance (yfinance)')
                        else:
                            umsatz_antworten.append(f'⚠️ Keine Umsatzdaten für {ticker} im Bereich {jahr_start}-{jahr_ende} gefunden.\nQuelle: Yahoo Finance (yfinance)')
                        continue
                    umsatz_antworten.append(f'⚠️ Umsatzdaten für {ticker} konnten nicht gefunden werden.\nQuelle: Yahoo Finance (yfinance)')
                except Exception as e:
                    umsatz_antworten.append(f'❌ Fehler beim Abrufen der Umsatzdaten für {ticker}: {e}\nQuelle: Yahoo Finance (yfinance)')
            return "\n\n".join(umsatz_antworten)
        # Schlüsselwörter für Umsatz und Gewinn (deutsch/englisch)
        revenue_keywords = ["umsatz", "revenue"]
        net_income_keywords = ["net income", "gewinn", "nettoergebnis", "nettoeinkommen"]
        # Umsatzbereich (Range) auch auf englisch erkennen
        umsatz_bereich = re.search(r'(20\d{2})\s*(?:bis|-|–|—|to)\s*(20\d{2})', input_lower)
        umsatz_bereich_start = umsatz_bereich.group(1) if umsatz_bereich else None
        umsatz_bereich_ende = umsatz_bereich.group(2) if umsatz_bereich else None
        # Umsatz und/oder Gewinn für ein Jahr (z.B. 2021)
        if any(kw in input_lower for kw in revenue_keywords + net_income_keywords):
            umsatz_antworten = []
            for name, ticker in gewuenschte_ticker:
                try:
                    stock = yf.Ticker(ticker)
                    fin = stock.financials
                    if fin is not None and not fin.empty:
                        antwort = []
                        # Umsatz für ein bestimmtes Jahr
                        jahr_match = re.search(r'(20\d{2})', input_lower)
                        jahr_gewünscht = jahr_match.group(1) if jahr_match else None
                        if any(kw in input_lower for kw in revenue_keywords) and 'Total Revenue' in fin.index:
                            revenue = fin.loc['Total Revenue']
                            revenue = revenue.sort_index()
                            years = [str(d.year) for d in revenue.index]
                            values = revenue.values / 1e9
                            if jahr_gewünscht:
                                if jahr_gewünscht in years:
                                    idx = years.index(jahr_gewünscht)
                                    antwort.append(f"Revenue of {ticker} in {jahr_gewünscht}: {values[idx]:.2f} bn USD\nQuelle: Yahoo Finance (yfinance)")
                                else:
                                    antwort.append(f"NOT_FOUND_YEAR: Revenue for {ticker} in {jahr_gewünscht} not available in yfinance.\nQuelle: Yahoo Finance (yfinance)")
                            else:
                                antwort.append(", ".join([f"{jahr}: {val:.2f} bn USD" for jahr, val in zip(years, values)]) + "\nQuelle: Yahoo Finance (yfinance)")
                        # Net Income für ein bestimmtes Jahr
                        if any(kw in input_lower for kw in net_income_keywords) and 'Net Income' in fin.index:
                            net_income = fin.loc['Net Income']
                            net_income = net_income.sort_index()
                            years = [str(d.year) for d in net_income.index]
                            values = net_income.values / 1e9
                            if jahr_gewünscht:
                                if jahr_gewünscht in years:
                                    idx = years.index(jahr_gewünscht)
                                    antwort.append(f"Net Income of {ticker} in {jahr_gewünscht}: {values[idx]:.2f} bn USD\nQuelle: Yahoo Finance (yfinance)")
                                else:
                                    antwort.append(f"NOT_FOUND_YEAR: Net Income for {ticker} in {jahr_gewünscht} not available in yfinance.\nQuelle: Yahoo Finance (yfinance)")
                            else:
                                antwort.append(", ".join([f"{jahr}: {val:.2f} bn USD" for jahr, val in zip(years, values)]) + "\nQuelle: Yahoo Finance (yfinance)")
                        if antwort:
                            umsatz_antworten.append("\n".join(antwort))
                        else:
                            umsatz_antworten.append(f'⚠️ No revenue/net income data found for {ticker} in financials.\nQuelle: Yahoo Finance (yfinance)')
                        continue
                    umsatz_antworten.append(f'⚠️ No financial data found for {ticker}.\nQuelle: Yahoo Finance (yfinance)')
                except Exception as e:
                    umsatz_antworten.append(f'❌ Error retrieving data for {ticker}: {e}\nQuelle: Yahoo Finance (yfinance)')
            return "\n\n".join(umsatz_antworten)
        else:
            return "ℹ️ Bitte stelle eine Frage zur Prognose, zum Umsatz oder zu einem Diagramm.\nQuelle: Yahoo Finance (yfinance)"
        return "\n\n".join(antworten)

    def __call__(self, input_text: str) -> str:
        return asyncio.run(self.invoke(input_text))
