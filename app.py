import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FORESIGHT Dashboard", layout="wide")

@st.cache_data
def load_data():
    risk = pd.read_excel("sku_risk_scores.xlsx", engine="openpyxl")
    weekly = pd.read_excel("weekly_with_lgb_predictions.xlsx", engine="openpyxl")

    risk.columns = [str(c).strip().lower().replace(" ", "_") for c in risk.columns]
    weekly.columns = [str(c).strip().lower().replace(" ", "_") for c in weekly.columns]

    weekly["week_start"] = pd.to_datetime(weekly["week_start"], errors="coerce")
    return risk, weekly

risk, weekly = load_data()

st.title("Project FORESIGHT")
st.write("Demand Forecasting & Inventory Risk — NorthBay Living")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total SKUs", len(risk))
c2.metric("HEALTHY", int((risk["action"] == "HEALTHY").sum()))
c3.metric("REORDER", int((risk["action"] == "REORDER").sum()))
c4.metric("MARKDOWN", int((risk["action"] == "MARKDOWN / REDUCE").sum()))
c5.metric("Sales at Risk (Rs)", f"{pd.to_numeric(risk['sales_at_risk'], errors='coerce').fillna(0).sum():,.0f}")

st.markdown("---")

st.subheader("Action counts")
st.bar_chart(risk["action"].value_counts())
