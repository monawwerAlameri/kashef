# Kashef — AI-Based Medication Recognition and Simplification System
Flask + SQLite + Bootstrap 5 (AR/EN, RTL/LTR). Follows the report: OCR → AI analysis → simplified results → history (three-tier).

## Run
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python app.py                  # http://127.0.0.1:5000
```
## Install Tesseract OCR (required for text extraction)
- Windows: https://github.com/UB-Mannheim/tesseract/wiki — tick **Arabic** during setup, then set `TESSERACT_CMD` in `config.py`
  (e.g. `C:\Program Files\Tesseract-OCR\tesseract.exe`).
- Ubuntu: `sudo apt install tesseract-ocr tesseract-ocr-ara`  | macOS: `brew install tesseract tesseract-lang`

## Default admin
`admin@kashef.com` / `Admin@123`  (change in `config.py` or env vars `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `SECRET_KEY`).

## Structure
| Path | Role (from the report) |
|---|---|
| `app.py` | Routes / application layer |
| `models.py` | Data layer: Users, Medicines, Dosages, Warnings, QR_Codes, AnalysisHistory |
| `services/ocr_service.py` | OCRProcessor (enhance + Tesseract ara+eng) |
| `services/ai_service.py` | AIAnalyzer (rule-based; swap with an LLM API later) |
| `translations.py` | Arabic / English texts |
| `templates/`, `static/` | Presentation layer |
