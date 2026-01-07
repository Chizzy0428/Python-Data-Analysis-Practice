import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# For older pandas versions (e.g., < 1.3.0)
import pandas as pd
import subprocess
import os


# Initialize git repository
if not os.path.exists('.git'):
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'config', 'user.name', 'Your Name'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'your.email@example.com'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)
    # Replace with your repo URL
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/username/repo.git'], check=True)
    subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
# load data set
df = pd.read_csv(
    r"C:\Users\VICTOR\cleaned_loan_data.csv",
    encoding="utf-8"
)

# title block
st.title('Bank Customer Loan Analysis')
st.write('interactive dashboard to analyze loans and risk')

###
df['Loan_Status']=df['Loan_Status'].str.strip().str.lower()
df['Approved_loan']=(df['Loan_Status']=='y').astype(int)

total_approved_loan = df['Approved_loan'].sum()
## income level
def incomelevel(CoapplicantIncome):
    if 	CoapplicantIncome <5000.0:
        return 'low'

    elif CoapplicantIncome <1000.0:
        return "Mid"

    else:
        return "High"
df["incomelevel"] = df['CoapplicantIncome'].apply(incomelevel)

# display matrix
st.metric(label="Total Approved Loan", value=total_approved_loan)
st.metric('Total people owing', df['is_owning'].sum())
st.metric('Default Rate', f"{df['Approved_loan'].mean():.2%}")


# create bands
# potential risk
low = df['Credit_History'].quantile(0.00)
high = df['Credit_History'].quantile(1.00)

def credit_bands(Credit_History):
    if Credit_History<=low:
        return 'low'

    elif Credit_History<=high:
        return 'mid'

    else:
        return'High'

df['credit_bands']=df['Credit_History'].apply(credit_bands)

# bar chart
credit_count = df['credit_bands'].value_counts().reset_index()
st.subheader('Credit History Bands')
#st.bar_chart(credit_count, x='index', y='credit_bands')
st.bar_chart(credit_count, x='credit_bands', y='count')
Loan_Amount_Term = df['Loan_Amount_Term'].value_counts()

# histogram


fig, ax = plt.subplots()
ax.hist(df['LoanAmount'], bins=20)
ax.set_xlabel("Loan Amount")
ax.set_ylabel("Frequency")

st.pyplot(fig)





