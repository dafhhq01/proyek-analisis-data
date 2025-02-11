import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_apa(day_df):
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df["year"] = day_df["dteday"].dt.year  
    
    jumlah_perhari_df = day_df.groupby(['year', 'season', 'weathersit']).agg({
        "instant": "nunique",
        "cnt": "sum"
    }).reset_index()
    
    jumlah_perhari_df.rename(columns={
        "instant": "order_count",
        "cnt": "penyewaan"
    }, inplace=True)
    
    jumlah_perhari_df["season_year"] = jumlah_perhari_df["season"].astype(str) + " " + jumlah_perhari_df["year"].astype(str)
    

    heatmap_df = day_df.groupby(['season', 'weathersit']).agg({
        "cnt": "sum"
    }).reset_index()
    heatmap_df.rename(columns={"cnt": "penyewaan"}, inplace=True)
    
    return jumlah_perhari_df, heatmap_df

#Membaca day_df.csv
day_df = pd.read_csv("dashboard/day_df.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(drop=True, inplace=True)

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/dafhhq01/proyek-analisis-data/main/cycling.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]
jumlah_perhari_df, heatmap_df = create_apa(main_df)

st.header('Dashboard Penyewaan Sepeda')

#Visualisasi pertama
st.subheader("Jumlah Penyewaan Berdasarkan Musim dan Kondisi Cuaca")
pivot_table = heatmap_df.pivot(index="season", columns="weathersit", values="penyewaan")
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, cmap="Blues", fmt=".0f", linewidths=0.5)
plt.title("Jumlah Penyewaan Berdasarkan Musim dan Kondisi Cuaca")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Musim")
st.pyplot(plt)

#Visualisasi kedua
st.subheader("Jumlah Penyewaan Berdasarkan Musim, Tahun, dan Kondisi Cuaca")
plt.figure(figsize=(12, 6))
sns.barplot(data=jumlah_perhari_df, x="season_year", y="order_count", hue="weathersit", palette="coolwarm")
plt.title("Jumlah Penyewaan Berdasarkan Musim, Tahun, dan Kondisi Cuaca", fontsize=14)
plt.xlabel("Musim dan Tahun")
plt.ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
plt.legend(title="Kondisi Cuaca")
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

st.caption('Copyright (c) Dicoding 2023')
