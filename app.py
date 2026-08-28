import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="FORESIGHT Dashboard", layout="wide")

def find_file(name):
    """Check root and data/ folder"""
    for p in [name, os.path.join("data", name)]:
        if os.path.exists(p):
            return p
    return None

@st.cache_data
def load_risk():
    path = find_file("sku_risk_scores.xlsx")
    if path is None:
        st.error("sku_risk_scores.xlsx not found in root or data/")
        st.stop()
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df

risk = load_risk()

st.title("Project FORESIGHT")
st.write("Demand Forecasting & Inventory Risk — NorthBay Living")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total SKUs", len(risk))
c2.metric("HEALTHY", int((risk["action"] == "HEALTHY").sum()))
c3.metric("REORDER", int((risk["action"] == "REORDER").sum()))
c4.metric("MARKDOWN", int((risk["action"] == "MARKDOWN / REDUCE").sum()))
c5.metric(
    "Sales at Risk (Rs)",
    f"{pd.to_numeric(risk['sales_at_risk'], errors='coerce').fillna(0).sum():,.0f}"
)

st.markdown("---")
st.subheader("Action counts")
st.bar_chart(risk["action"].value_counts())

st.subheader("SKU Risk Table")
cols = [c for c in [
    "sku_id", "category", "action", "forecast",
    "inventory_position", "weeks_of_cover",
    "sales_at_risk", "locked_capital"
] if c in risk.columns]
st.dataframe(
    risk[cols].sort_values("sales_at_risk", ascending=False),
    use_container_width=True,
    height=350
)

left, right = st.columns(2)

with left:
    st.subheader("Top REORDER (Sales at Risk)")
    reorder = risk[risk["action"] == "REORDER"].copy()
    reorder["sales_at_risk"] = pd.to_numeric(reorder["sales_at_risk"], errors="coerce").fillna(0)
    reorder = reorder.nlargest(10, "sales_at_risk")
    if len(reorder) > 0:
        st.plotly_chart(
            px.bar(reorder, x="sales_at_risk", y="sku_id", orientation="h",
                   color="sales_at_risk", color_continuous_scale="Reds"),
            use_container_width=True
        )
    else:
        st.info("No REORDER SKUs")

with right:
    st.subheader("Top MARKDOWN (Locked Capital)")
    md = risk[risk["action"] == "MARKDOWN / REDUCE"].copy()
    md["locked_capital"] = pd.to_numeric(md["locked_capital"], errors="coerce").fillna(0)
    md = md.nlargest(10, "locked_capital")
    if len(md) > 0:
        st.plotly_chart(
            px.bar(md, x="locked_capital", y="sku_id", orientation="h",
                   color="locked_capital", color_continuous_scale="Oranges"),
            use_container_width=True
        )
    else:
        st.info("No MARKDOWN SKUs")

st.caption("LightGBM WAPE 19.96% | Baseline 31.26% | Project FORESIGHT")
