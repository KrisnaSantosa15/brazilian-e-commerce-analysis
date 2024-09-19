import urllib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from babel.numbers import format_currency
import streamlit as st

sns.set(style='dark')


def create_rfm_df(df):
    rfm_dataframe = df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",    # Mengambil tanggal order terakhir
        "customer_id": "nunique",  # Menghitung jumlah order (frequency)
        "price": "sum"    # Menghitung total revenue (monetary)
    })

    rfm_dataframe.columns = ["customer_id",
                             "max_order_timestamp", "frequency", "monetary"]

    # Menghitung nilai recency berdasarkan tanggal terakhir order (berapa hari sejak transaksi terakhir)
    rfm_dataframe["max_order_timestamp"] = rfm_dataframe["max_order_timestamp"].dt.date
    # Mendapatkan tanggal terakhir dalam dataset
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_dataframe["recency"] = rfm_dataframe["max_order_timestamp"].apply(
        lambda x: (recent_date - x).days)

    rfm_dataframe.drop("max_order_timestamp", axis=1, inplace=True)

    return rfm_dataframe


def plot_brazil_map(data):
    brazil = mpimg.imread(urllib.request.urlopen(
        'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')

    figure, ax = plt.subplots()  # Adjust figuresize as needed
    data.plot(kind="scatter", x="geolocation_lng",
              y="geolocation_lat", ax=ax, alpha=0.3, s=0.3, c='blue')
    ax.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
    ax.axis('off')

    st.pyplot(figure)


def get_customer_count(df, ascending=False):
    state_full_names = {
        'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
        'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
        'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
        'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
        'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
    }

    state_customer_counts = df.groupby('geolocation_state')[
        'customer_unique_id'].nunique().reset_index(name='customer_count')

    state_customer_counts_sorted = state_customer_counts.sort_values(
        by='customer_count', ascending=ascending)

    state_abbr = state_customer_counts_sorted.iloc[0]['geolocation_state']
    customer_count = state_customer_counts_sorted.iloc[0]['customer_count']
    state_full_name = state_full_names.get(state_abbr, 'Unknown State')

    return customer_count, state_full_name


# Load Data
all_data = pd.read_csv("all_data.csv")

datetime_columns = ['order_purchase_timestamp', 'order_approved_at',
                    'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

# Sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://imgs.search.brave.com/dhIlMrBdOvliOehbxCFjP3pMm607rL1JE1qrNTEOQho/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/YnJhbmRmZXRjaC5p/by9pZHZTbjRPcmc1/L3RoZW1lL2Rhcmsv/bG9nby5zdmc_az1p/ZDY0TXVwN2FjJnQ9/MTcxNzAwMTE5OTM1/Mz90PTE3MTcwMDEx/OTkzNTM")

    st.text("Olist E-commerce Dashboard")
    st.text("by Krisna Santosa")

rfm_df = create_rfm_df(all_data)


# Visualisasi Data
st.header('Olist E-Commerce Dashboard :sparkles:')

# Best & Worst Performing Product
st.subheader("Best & Worst Performing Product Category")

# Hitung jumlah pesanan per kategori produk
order_category_df = all_data.groupby('product_category_name_english')[
    'order_id'].nunique().reset_index(name='order_count')

# Sort untuk kategori terbaik dan terburuk
best_categories = order_category_df.sort_values(
    by='order_count', ascending=False).head(5)
worst_categories = order_category_df.sort_values(
    by='order_count', ascending=True).head(5)

# Visualisasi
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Plot kategori terbaik
sns.barplot(x="order_count", y="product_category_name_english",
            data=best_categories, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Jumlah Pesanan')
ax[0].set_title("Best Performing Category", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

# Plot kategori terburuk
sns.barplot(x="order_count", y="product_category_name_english",
            data=worst_categories, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('Jumlah Pesanan')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Best and Worst Performing Category by Order Count", fontsize=20)
# plt.show()

st.pyplot(fig)

# Customer Demographics
st.subheader("Customer Demographics")

column1, column2 = st.columns(2)

with column1:
    # Most Active Customer
    most_customer = get_customer_count(all_data, ascending=False)
    st.text("Most Active Customer State")
    st.metric("State: " + str(most_customer[1]), value=most_customer[0])

with column2:
    # Least Active Customer
    least_customer = get_customer_count(all_data, ascending=True)
    st.text("Least Active Customer State")
    st.metric("State: " + str(least_customer[1]), value=least_customer[0])

col1, col2 = st.columns(2)

with col1:
    # Load brazil map
    brazil_plain = mpimg.imread(urllib.request.urlopen(
        'https://gisgeography.com/wp-content/uploads/2024/05/Brazil-Map-1536x1536.jpg'), 'jpg')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(brazil_plain)
    ax.axis('off')
    # plt.show()
    st.pyplot(fig)

with col2:
    plot_brazil_map(all_data.drop_duplicates(subset='customer_unique_id'))

# fig, ax = plt.subplots(figsize=(20, 10))
# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3",
#           "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# sns.barplot(
#     x="customer_count",
#     y="state",
#     data=bystate_df.sort_values(by="customer_count", ascending=False),
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Number of Customer by States", loc="center", fontsize=30)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
# st.pyplot(fig)


# RFM Analysis
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(
        rfm_df.monetary.mean(), "BRL", locale='pt_BR')
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(
    by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45, ha='right')
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(
    by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45, ha='right')

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(
    by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=45, ha='right')

st.pyplot(fig)

st.caption('Copyright (c) Krisna Santosa 2024')
