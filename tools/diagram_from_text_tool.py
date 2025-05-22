import matplotlib.pyplot as plt
import re
import uuid
import os

class DiagramFromTextTool:
    name = "DiagramFromTextTool"
    description = "Erstellt ein Umsatzdiagramm aus einem gegebenen Text mit Jahres-Umsatz-Paaren."

    def __call__(self, input_text: str) -> str:
        # Robustere Extraktion: Jahr und Umsatz in Sätzen wie 'Im Jahr 2024 ... 348,16 Milliarden ...'
        # 1. Versuche: Jahr: Wert ...
        matches = re.findall(r"(20\d{2})[^\d]{0,20}(\d+[\.,]?\d*)[^\d]{0,20}(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", input_text, re.IGNORECASE)
        # 2. Versuche: 'Im Jahr 2024 ... 348,16 Milliarden ...'
        if not matches:
            matches = re.findall(r"(?:im|in|für)? ?jahr[\s:]*?(20\d{2})[^\d]{0,40}?(\d+[\.,]?\d*)[^\d]{0,20}(Mrd|Milliarden|bn|Billion|Billionen|USD|EUR|Won|Euro|Dollar)", input_text, re.IGNORECASE)
        if not matches:
            return "⚠️ Keine Umsatzdaten im Text gefunden. Bitte gib die Werte als 'Jahr: Umsatz' an."
        years = []
        values = []
        for year, value, _ in matches:
            years.append(year)
            value = value.replace(",", ".")
            try:
                values.append(float(value))
            except Exception:
                values.append(None)
        filtered = [(y, v) for y, v in zip(years, values) if v is not None]
        if not filtered:
            return "⚠️ Keine gültigen Umsatzwerte gefunden."
        years, values = zip(*filtered)
        plt.figure(figsize=(8,4))
        plt.bar(years, values, color='royalblue')
        plt.title('Umsatz (aus Webdaten)')
        plt.xlabel('Jahr')
        plt.ylabel('Umsatz (Originaleinheit)')
        plt.grid(axis='y')
        fname = f'web_umsatz_{uuid.uuid4().hex}.png'
        plt.savefig(fname)
        plt.close()
        return f'📊 Diagramm aus Webdaten gespeichert unter: {fname}'

diagram_from_text_tool = DiagramFromTextTool()
