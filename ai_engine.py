# ai_engine.py
import google.generativeai as genai
import os
import json
import streamlit as st
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_statement(uploaded_file):
    """
    Sends the PDF file to Gemini and returns a python dictionary (JSON).
    """
    # Configure the model to ALWAYS return JSON
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Read file bytes
    file_bytes = uploaded_file.getvalue()
    
    # The Prompt
    prompt = """
    You are a senior financial analyst. I am providing a bank statement PDF.
    Analyze the transaction history and extract the following details. 
    
    Required JSON Fields:
    - "monthly_salary": (Estimate the recurring monthly salary/income credits. Return a number.)
    - "total_emis": (Sum of likely loan repayments or EMI deductions per month. Return a number.)
    - "closing_balance_avg": (Average closing balance over the period. Return a number.)
    - "bounced_checks": (Count of declined/bounced transactions. Return a number.)
    
    If you cannot find a value, estimate it based on patterns or set it to 0.
    """
    
    try:
        # Generate content
        response = model.generate_content([
            {'mime_type': 'application/pdf', 'data': file_bytes},
            prompt
        ])
        
        # Parse the JSON directly
        return json.loads(response.text)
        
    except Exception as e:
        # This will now show the EXACT error in your terminal/app
        st.error(f"Technical Error: {e}")
        return None

# --- NEW CHAT FUNCTION ---
def chat_with_data(user_query, financial_data):
    """
    Answers user questions based purely on the extracted financial data.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    You are a helpful, professional financial AI assistant. 
    Here is the user's extracted bank statement data:
    {json.dumps(financial_data, indent=2)}
    
    Answer the user's question based ONLY on this data and general financial best practices. 
    Keep the answer concise and helpful.
    
    User Question: {user_query}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"