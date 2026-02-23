# app.py
import streamlit as st
import ai_engine  
import pandas as pd 
import logic   
import plotly.graph_objects as go    
import time
import base64  # <-- NEW IMPORT FOR PDF VIEWER

# --- 1. PAGE SETUP & STYLING ---
st.set_page_config(
    page_title="Loan Eligibility Checker", 
    page_icon="🏦", 
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
    st.markdown("## ⚙️ Analysis Parameters")
    st.info("This AI agent analyzes bank statements to calculate Debt-to-Income (DTI) ratios, average balances, and risk factors to recommend loan products.")
    
    # --- NEW ADDITIONS TO THE SIDEBAR ---
    st.markdown("### 🔍 Key Metrics Evaluated")
    st.markdown("""
    * 📈 **Income Stability** (Recurring credits)
    * 📉 **Debt Burden** (Active EMIs)
    * 💰 **Liquidity** (Average daily balance)
    * ⚠️ **Risk Indicators** (Bounced cheques)
    """)
    
    st.markdown("<br>", unsafe_allow_html=True) # Adds a little spacing
    
    with st.expander("🤖 View AI Engine Specs"):
        st.caption("**Core Model:** Gemini 2.5 Flash")
        st.caption("**Extraction Protocol:** Multimodal Vision to JSON")
        st.caption("**Security:** Zero-Retention Processing")
        st.caption("**Estimated Latency:** ~1.5s")
    # -----------------------------------

    st.markdown("---")
    st.markdown("### 🔒 Privacy Secure")
    st.caption("Documents are processed strictly for real-time analysis and are not permanently stored on any server.")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .gradient-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00E676, #00B4DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #A0AEC0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stFileUploadDropzone"] {
        border: 2px dashed #00B4DB;
        background-color: rgba(0, 180, 219, 0.05);
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    div[data-testid="stFileUploadDropzone"]:hover {
        border-color: #00E676;
        background-color: rgba(0, 230, 118, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER SECTION ---
st.markdown('<h1 class="gradient-title">🏦 AI Loan Eligibility & Health Checker</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Upload your Bank Statement (PDF) to instantly analyze your financial health score and discover pre-approved loan options.</p>', unsafe_allow_html=True)

st.divider()

# --- 3. SESSION STATE INITIALIZATION ---
if "financial_data" not in st.session_state:
    st.session_state.financial_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_bytes" not in st.session_state:  # <-- NEW STATE TO REMEMBER THE PDF
    st.session_state.pdf_bytes = None

# --- 4. MAIN APP LOGIC ---
uploaded_file = st.file_uploader("Drop your Bank Statement (PDF) here", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 Analyze Financial Profile", use_container_width=True):
        with st.spinner("🤖 Gemini is analyzing transaction history..."):
            time.sleep(1) 
            st.session_state.financial_data = ai_engine.analyze_statement(uploaded_file)
            st.session_state.chat_history = []
            
            # Save the raw PDF bytes into memory so we can show it on screen
            st.session_state.pdf_bytes = uploaded_file.getvalue() 
            
    # If we have data AND the PDF saved in memory, display the UI
    if st.session_state.financial_data and st.session_state.pdf_bytes:
        st.success("Analysis Complete!")
        st.divider()
        
        # --- NEW: SIDE-BY-SIDE LAYOUT ---
        # Splitting the screen into two massive columns (PDF on left, Dashboard on right)
        pdf_col, dash_col = st.columns([1, 1.2], gap="large")
        
        # ==========================================
        # LEFT COLUMN: THE PDF VIEWER
        # ==========================================
        with pdf_col:
            st.subheader("📄 Original Statement")
            
            # Convert PDF bytes to base64 so HTML can render it
            base64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
            
            # Embed the PDF using an HTML iframe
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        # ==========================================
        # RIGHT COLUMN: THE DASHBOARD
        # ==========================================
        with dash_col:
            # --- HUMAN-IN-THE-LOOP (EDITABLE DATA) ---
            st.subheader("✍️Verify AI Extraction")
            
            df = pd.DataFrame([st.session_state.financial_data])
            edited_df = st.data_editor(df, width="stretch", hide_index=True)
            verified_data = edited_df.iloc[0].to_dict()
            
            salary = int(verified_data.get('monthly_salary', 0))
            balance = int(verified_data.get('closing_balance_avg', 0))
            emis = int(verified_data.get('total_emis', 0))
            bounces = int(verified_data.get('bounced_checks', 0))
            
            my_score = logic.calculate_custom_score(verified_data)
            eligible_loans = logic.check_loan_eligibility(salary, my_score)
            
            st.divider()

            # --- DASHBOARD UI ---
            st.subheader("📊Financial Overview")
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric(label="Estimated Salary", value=f"₹{salary:,}")
            metric_col2.metric(label="Avg Balance", value=f"₹{balance:,}")
            metric_col3.metric(label="Current EMIs", value=f"₹{emis:,}", delta=f"{(emis/salary)*100:.1f}% DTI" if salary > 0 else None, delta_color="inverse")
            
            st.divider()

            # --- SCORE & LOANS UI ---
            score_col, loans_col = st.columns([1, 1], gap="medium")
            
            with score_col:
                st.subheader("🎯 Health Score")
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = my_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "white", 'thickness': 0.15},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [300, 649], 'color': "#dc3545"}, 
                            {'range': [650, 749], 'color': "#ffc107"}, 
                            {'range': [750, 900], 'color': "#28a745"}  
                        ],
                    }
                ))
                fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)

            with loans_col:
                st.subheader("💸 Cash Flow")
                remaining_income = max(0, salary - emis)
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Available', 'EMIs'], 
                    values=[remaining_income, emis], 
                    hole=.5, 
                    marker_colors=['#00B4DB', '#FF4B4B'], 
                    textinfo='label+percent'
                )])
                fig_pie.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
                st.plotly_chart(fig_pie, use_container_width=True)

            # Pre-Qualified Offers
            st.subheader("✅ Pre-Qualified Offers")
            if eligible_loans:
                for loan in eligible_loans:
                    with st.container(border=True): 
                        st.write(f"**{loan['bank']}** | {loan['loan_type']} | 📉 Interest: {loan['interest']}")
            else:
                st.info("No specific loan products match this profile right now.")

            st.divider()

            # --- EXPORT FEATURE ---
            export_df = pd.DataFrame([verified_data])
            export_df['calculated_score'] = my_score
            csv_data = export_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Report (CSV)", data=csv_data, file_name='report.csv', mime='text/csv', width="stretch")

            # --- CHAT WITH DATA ---
            st.divider()
            st.subheader("💬 Ask the AI")
            
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ask about these finances..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        ai_response = ai_engine.chat_with_data(prompt, verified_data)
                        st.markdown(ai_response)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})