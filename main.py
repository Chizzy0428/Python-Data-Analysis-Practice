import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="Bank Customer Loan Analysis",
    layout="wide"
)

st.title("🏦 Bank Customer Loan Analysis")
st.write("Interactive dashboard to analyze loan approvals and credit risk")

# -----------------------------
# Load Data (Same Repo)
# -----------------------------
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "cleaned_loan_data.csv")
    return pd.read_csv(file_path)

df = load_data()

# -----------------------------
# Data Cleaning & Features
# -----------------------------
df["Loan_Status"] = df["Loan_Status"].str.strip().str.lower()
df["Approved_loan"] = (df["Loan_Status"] == "y").astype(int)

# Income level classification
def income_level(co_income):
    if co_income < 1000:
        return "Low"
    elif co_income < 5000:
        return "Mid"
    else:
        return "High"

df["income_level"] = df["CoapplicantIncome"].apply(income_level)

# Credit history bands (quantile-based)
low_q = df["Credit_History"].quantile(0.33)
high_q = df["Credit_History"].quantile(0.66)

def credit_band(value):
    if value <= low_q:
        return "Low"
    elif value <= high_q:
        return "Mid"
    else:
        return "High"

df["credit_band"] = df["Credit_History"].apply(credit_band)

# -----------------------------
# Key Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Approved Loans", int(df["Approved_loan"].sum()))
col2.metric("Total People Owing", int(df["is_owning"].sum()))
col3.metric("Approval Rate", f"{df['Approved_loan'].mean():.2%}")

# -----------------------------
# Credit Band Distribution
# -----------------------------
st.subheader("📊 Credit History Bands")

credit_counts = (
    df["credit_band"]
    .value_counts()
    .reset_index()
)

credit_counts.columns = ["Credit Band", "Count"]

st.bar_chart(
    credit_counts,
    x="Credit Band",
    y="Count"
)

# -----------------------------
# Loan Amount Distribution
# -----------------------------
st.subheader("📈 Loan Amount Distribution")

fig, ax = plt.subplots()
ax.hist(df["LoanAmount"].dropna(), bins=20)
ax.set_xlabel("Loan Amount")
ax.set_ylabel("Frequency")

st.pyplot(fig)
