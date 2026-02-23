# 🏦 AI Loan Eligibility & Health Checker

An end-to-end FinTech application that extracts unstructured data from bank statement PDFs to calculate custom financial health scores, assess creditworthiness, and recommend pre-qualified loan products.

## 🧠 Project Overview
Traditional loan processing requires manual review of bank statements to calculate Income and Debt-to-Income (DTI) ratios. This project automates that pipeline using Generative AI (Google Gemini 2.5 Flash) to parse transaction histories, identify risk factors (like bounced cheques), and visually present the data in a business-ready dashboard.

## ✨ Key Features
* **🤖 AI Document Parsing:** Utilizes Gemini's multimodal capabilities to extract key metrics (`monthly_salary`, `total_emis`, `closing_balance`) directly from raw PDFs.
* **✍️ Human-in-the-Loop Validation:** Includes an interactive data grid allowing users to verify and edit AI-extracted numbers before final scoring.
* **📊 Dynamic Visualization:** Built with Streamlit and Plotly to render real-time Gauge Charts (Health Score) and Donut Charts (Cash Flow).
* **💬 Chat with Data:** An integrated AI assistant that answers specific user queries based purely on their uploaded financial context.
* **📄 Side-by-Side PDF Viewer:** Native rendering of the original bank document alongside the analytics dashboard for seamless UX.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Frontend/UI:** Streamlit
* **AI Engine:** Google Generative AI (Gemini 2.5 Flash API)
* **Data Processing:** Pandas, JSON
* **Visualizations:** Plotly
* **Utilities:** FPDF (for generating dummy test data), base64

