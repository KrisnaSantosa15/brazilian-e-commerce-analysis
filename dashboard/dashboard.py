import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from babel.numbers import format_currency

st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("📊 Customer Segmentation Dashboard")


@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    datetime_cols = ['order_purchase_timestamp', 'order_approved_at',
                     'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])
    return df


all_data = load_data()

# Sidebar Settings
with st.sidebar:
    st.title("Olist E-Commerce Dashboard")
    st.image("https://as2.ftcdn.net/v2/jpg/00/90/67/29/1000_F_90672947_9o36fMzvYpFoS2cvgxACFUR0wleV5Yq5.jpg")
    st.subheader("Filter Data by Date 📅")

    # Date Selection
    min_date, max_date = all_data["order_purchase_timestamp"].min(
    ).date(), all_data["order_purchase_timestamp"].max().date()

    # Set Default Start Date to 2018-01-01 to prevent large data load
    default_start_date = max(min_date, pd.to_datetime("2018-08-01").date())

    st.write("Select the date range below:")

    start_date = st.date_input(
        "Start Date", value=default_start_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("End Date", value=max_date,
                             min_value=min_date, max_value=max_date)
    st.write(f"Data available from {min_date} to {max_date}")

# Filter Data by Date
filtered_data = all_data[
    (all_data["order_purchase_timestamp"].dt.date >= start_date) &
    (all_data["order_purchase_timestamp"].dt.date <= end_date)
]


# Main Content
st.subheader("🌍 Customer Geographic Distribution")
fig = px.scatter_geo(filtered_data, lat="geolocation_lat", lon="geolocation_lng",
                     hover_name="customer_city", color="customer_state",
                     title="Customer Locations in Brazil")
st.plotly_chart(fig)


# Customer Segmentation
st.subheader("🏆 Best & Worst Performing Product Categories")

order_category_df = filtered_data.groupby('product_category_name_english')[
    'order_id'].nunique().reset_index(name='order_count')

best_categories = order_category_df.sort_values(
    by='order_count', ascending=False).head(5)
worst_categories = order_category_df.sort_values(
    by='order_count', ascending=True).head(5)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
sns.barplot(x="order_count", y="product_category_name_english",
            data=best_categories, ax=ax[0], palette="Blues")
sns.barplot(x="order_count", y="product_category_name_english",
            data=worst_categories, ax=ax[1], palette="Reds")
ax[0].set_title("Best Performing Categories")
ax[1].set_title("Worst Performing Categories")
st.pyplot(fig)


# Category Sales Analysis
st.subheader("📊 Category Sales Analysis")
selected_category = st.selectbox(
    "Select Product Category:", all_data["product_category_name_english"].unique())

category_data = filtered_data[filtered_data["product_category_name_english"]
                              == selected_category]

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=category_data,
             x="order_purchase_timestamp", y="price", ax=ax)
ax.set_title(f"Sales Trend for {selected_category}")
st.pyplot(fig)


# Customer Demographics
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Top Customers by Monetary Value")
    top_customers = filtered_data.groupby("customer_unique_id")[
        "price"].sum().reset_index()
    top_customers = top_customers.sort_values(
        by="price", ascending=False).head(10)
    st.dataframe(top_customers)


with col2:
    st.subheader("📌Business Insights")

    total_orders = len(filtered_data["order_id"].unique())
    total_customers = len(filtered_data["customer_unique_id"].unique())
    top_category = order_category_df.sort_values(
        by="order_count", ascending=False).iloc[0]["product_category_name_english"]

    st.markdown(f"""
    - 📦 **Total Orders**: {total_orders}
    - 👥 **Total Customers**: {total_customers}
    - 🏆 **Most Popular Category**: {top_category}
    """)


# Footer
st.caption('Copyright (c) Krisna Santosa 2025')
