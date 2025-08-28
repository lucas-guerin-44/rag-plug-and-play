import pdfplumber
import pandas as pd
from typing import List

def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def parse_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_csv(file_path: str) -> str:
    df = pd.read_csv(file_path)
    return df.to_csv(index=False)

def parse_file(file_path: str) -> str:
    print(file_path)
    if file_path.endswith(".txt"):
        return parse_txt(file_path)
    elif file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".csv"):
        return parse_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
