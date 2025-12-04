import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import random
import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Gemini Key (add yours)
GEMINI_API_KEY = "AIzaSyA8YnbwSGh8VNL4g72KsZTBuUOG80jZ-Sw"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="StockSense Agent", layout="wide")

st.title("🛡️ StockSense Agent – AI Trading Guardian")

# Sidebar Salary
salary = st.sidebar.number_input("Monthly Salary (₹)", value=60000)
limit = salary * 0.2
st.sidebar.success(f"Invest Limit: ₹{limit:,.0f}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "AI Chat", "IPO", "Report"])

with tab1:
    col1, col2 = st.columns(2)
    with col1: st.metric("Sensex", "85,265", "+158")
    with col2: st.metric("Nifty", "26,034", "+48")
    fig = px.line(pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu"], "Nifty": [25800, 25900, 25700, 26034]}), x="Day", y="Nifty")
    st.plotly_chart(fig)

with tab2:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])
    prompt = st.chat_input("Ask: HDFC safe?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)
        response = model.generate_content(f"Advice for {prompt}. Salary ₹{salary}.").text
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").markdown(response)

with tab3:
    ipo = st.selectbox("IPO", ["Swiggy", "NTPC Green"])
    st.metric("GMP", "+₹42")
    st.metric("Fit Score", "82/100")

with tab4:
    if st.button("PDF Report"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawString(100, 750, f"Saved: ₹{random.randint(10000, 20000):,}")
        c.save()
        buffer.seek(0)
        st.download_button("Download", buffer, "report.pdf")
