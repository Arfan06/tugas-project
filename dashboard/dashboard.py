import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name").order_id.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_city_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bycity_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

def create_byscore_df(df):
    byscore_df = df.groupby(by="review_score").customer_id.nunique().reset_index()
    byscore_df.rename(columns={
        "product_category_name": "product"
    }, inplace=True)
    byscore_df['review_score'] = pd.Categorical(byscore_df['review_score'], [1, 2, 3, 4, 5])
    
    return byscore_df

all_df = pd.read_csv("dashboard/all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_delivered_customer_date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    logo_url = "https://github.com/omgswap/public-assets/blob/master/assets/smartchain/0x4338665CBB7B2485A8855A139b75D5e34AB0DB94/logo.png"
    st.image(logo_url, use_container_width=True)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_delivered_customer_date"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
byscore_df = create_byscore_df(main_df)
bystate_df = create_bystate_df(main_df)

st.header('Arfan Collection :sparkles:')
st.subheader('Daily Orders')
col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Customer Rating")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="customer_id", 
    x="review_score",
    data=byscore_df.sort_values(by="customer_id", ascending=False),
    palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"],
    ax=ax
)
ax.set_title("Number of Customer by Rating", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.caption('Copyright (c) Ari Fansuri/Dicoding Course')
