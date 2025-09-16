import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Bank Loan Analysis Dashboard",
    page_icon="💰",
    layout="wide"
)

# -------------------- Load Data --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("financial_loan.csv")  # Make sure your dataset is cleaned and present
    return df

df = load_data()

# -------------------- Sidebar --------------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "Univariate Analysis", "Bivariate Analysis", "Time Trends", "Insights"])

# -------------------- Header --------------------
st.title("💰 Bank Loan Analysis Dashboard")
st.markdown("A professional EDA dashboard built with **Streamlit** to explore loan data interactively.")

# -------------------- KPIs --------------------
total_loans = df.shape[0]
avg_income = df["annual_income"].mean()
default_rate = (df["loan_status"].value_counts(normalize=True).get("Charged Off", 0)) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Loans", f"{total_loans:,}")
col2.metric("Avg Annual Income", f"${avg_income:,.0f}")
col3.metric("Default Rate", f"{default_rate:.2f}%")

st.markdown("---")

# -------------------- Pages --------------------
if page == "Overview":
    st.subheader("Dataset Snapshot")
    st.dataframe(df.head(20))

    st.subheader("Loan Status Distribution")
    fig = px.histogram(df, x="loan_status", color="loan_status", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Univariate Analysis":
    st.subheader("Univariate Analysis")

    col = st.selectbox("Select a column to explore", ["grade", "purpose", "home_ownership", "term"])
    fig = px.histogram(df, x=col, color="loan_status", barmode="group", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Bivariate Analysis":
    st.subheader("Bivariate Analysis")

    col_x = st.selectbox("Select X-axis variable", ["annual_income", "dti", "installment"])
    col_y = st.selectbox("Select Y-axis variable", ["loan_status", "grade", "purpose"])
    
    if col_y == "loan_status":
        fig = px.box(df, x="loan_status", y=col_x, color="loan_status")
    else:
        fig = px.scatter(df, x=col_x, y="total_payment", color=col_y, size="annual_income", hover_data=["grade"])
    
    st.plotly_chart(fig, use_container_width=True)

elif page == "Time Trends":
    st.subheader("Loan Issue Trends Over Time")

    # Fix: Explicit date format specified
    df["issue_year"] = pd.to_datetime(df["issue_date"], format="%d-%m-%Y", errors="coerce").dt.year

    trend = df.groupby("issue_year")["id"].count().reset_index()
    fig = px.line(trend, x="issue_year", y="id", markers=True, title="Number of Loans Issued Over Time")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Default Rates Over Time")
    default_trend = (
        df.groupby("issue_year")["loan_status"]
        .apply(lambda x: (x == "Charged Off").mean() * 100)
        .reset_index()
    )
    fig = px.line(default_trend, x="issue_year", y="loan_status", markers=True, title="Default Rate Over Time")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Insights":
    st.subheader("Key Insights")
    st.markdown("""
    - Loan defaults are higher in **lower grades (D, E, F, G)**.  
    - **Debt-to-Income (DTI)** ratio strongly correlates with loan default risk.  
    - Borrowers with **Rent/Mortgage homes** have higher default rates compared to owners.  
    - Loan purposes like **small business and debt consolidation** show more defaults.  
    - Default rates peaked around certain years, showing **economic impact** on repayments.  
    """)

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit | Bank Loan Analysis Project")
