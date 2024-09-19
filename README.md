# Brazilian E-Commerce RFM and Geospatial Analysis

Proyek ini merupakan proyek analisis data yang bertujuan untuk menganalisis data penjualan e-commerce di Brazil. Data yang digunakan berasal dari [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Proyek ini terdiri dari dua analisis, yaitu analisis RFM (Recency, Frequency, Monetary) dan analisis geospatial. Analisis RFM bertujuan untuk mengelompokkan pelanggan berdasarkan perilaku pembelian mereka, sedangkan analisis geospatial bertujuan untuk mengetahui sebaran pelanggan di Brazil.

## Dataset
Dataset yang digunakan dalam proyek ini terdiri dari beberapa file, yaitu:
1. `olist_customers_dataset.csv` - Data pelanggan
2. `olist_geolocation_dataset.csv` - Data geolokasi
3. `olist_order_items_dataset.csv` - Data item pesanan
4. `olist_orders_dataset.csv` - Data pesanan
5. `olist_products_dataset.csv` - Data produk
6. `product_category_name_translation.csv` - Data kategori produk

## Requirements
- Python 3.9
- Pandas
- Numpy
- Matplotlib
- Seaborn
- Streamlit


## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Run Streamlit App
```bash
streamlit run dashboard.py
```