# AI Loan Eligibility & Financial Score Checker

A Streamlit-based web application that analyzes bank statement PDFs using **Google Gemini AI** to calculate a financial health score and recommend suitable bank loans.

## Features

* **PDF Analysis:** Uses Google Gemini 1.5 Flash to parse complex bank statement PDFs.
* **Data Extraction:** Automatically extracts key financial metrics:
    * Monthly Salary / Income
    * Total Monthly EMIs / Obligations
    * Average Closing Balance
    * Bounced Cheques/Transactions
* **Smart Scoring:** Calculates a custom "Financial Health Score" (300-900) based on cash flow logic (similar to a CIBIL score).
* **Loan Matching:** Recommendations specific loans from a mock database based on the calculated score and salary eligibility.

## Tech Stack

* **Frontend:** Streamlit
* **AI Model:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **Language:** Python 3.x
* **Environment Management:** python-dotenv

## Project Structure

```text
├── app.py           # Main application file (Frontend UI)
├── ai_engine.py     # Handles interaction with Google Gemini API
├── logic.py         # Contains scoring math and loan rules
├── requirements.txt # List of python dependencies
├── .env             # Stores API keys (Not uploaded to GitHub)
└── README.md        # Project documentation