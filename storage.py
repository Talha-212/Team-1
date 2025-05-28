import pandas as pd
from fpdf import FPDF
import os

def save_result(name, wpm, accuracy, filename="results.csv"):
    df = pd.DataFrame([[name, wpm, accuracy]], columns=["Name", "WPM", "Accuracy"])
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

def get_leaderboard(filename="results.csv"):
    if not os.path.exists(filename):
        return None
    df = pd.read_csv(filename)
    return df.sort_values(by="WPM", ascending=False).head(5)

def export_pdf(name, wpm, accuracy, filename="typing_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Typing Speed Test Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"WPM: {wpm}", ln=True)
    pdf.cell(200, 10, txt=f"Accuracy: {accuracy}%", ln=True)
    pdf.output(filename)
