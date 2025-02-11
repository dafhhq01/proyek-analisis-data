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
    
    #Mengubah angka musim 
    season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    jumlah_perhari_df["season"] = jumlah_perhari_df["season"].map(season_mapping)
    
    jumlah_perhari_df["season_year"] = jumlah_perhari_df["season"] + " " + jumlah_perhari_df["year"].astype(str)

    #Mengubah angka kondisi cuaca 
    weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    jumlah_perhari_df["weathersit"] = jumlah_perhari_df["weathersit"].map(weather_mapping)

    heatmap_df = day_df.groupby(['season', 'weathersit']).agg({
        "cnt": "sum"
    }).reset_index()
    heatmap_df.rename(columns={"cnt": "penyewaan"}, inplace=True)

    heatmap_df["season"] = heatmap_df["season"].map(season_mapping)
    heatmap_df["weathersit"] = heatmap_df["weathersit"].map(weather_mapping)

    return jumlah_perhari_df, heatmap_df

#Membaca day_df.csv
day_df = pd.read_csv("dashboard/day_df.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(drop=True, inplace=True)

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/dafhhq01/proyek-analisis-data/main/dashboard/icon.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]
jumlah_perhari_df, heatmap_df = create_apa(main_df)

st.header('Dashboard Penyewaan Sepeda')

color_palette = {
    "Cerah": "#FFD700",         
    "Berawan": "#87CEEB",       
    "Hujan Ringan": "#4682B4",  
    "Hujan Lebat": "#2F4F4F"    
}

#Visualisasi pertama 
st.subheader("Jumlah Penyewaan Berdasarkan Musim dan Kondisi Cuaca")
plt.figure(figsize=(10, 6))
sns.barplot(data=heatmap_df, x="season", y="penyewaan", hue="weathersit", palette=color_palette)
plt.title("Jumlah Penyewaan Berdasarkan Musim dan Kondisi Cuaca")
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan")
plt.legend(title="Kondisi Cuaca")
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

#Visualisasi kedua 
st.subheader("Jumlah Penyewaan Berdasarkan Musim, Tahun, dan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))


season_years = jumlah_perhari_df["season_year"].unique()
weathersits = jumlah_perhari_df["weathersit"].unique()

bottom_values = [0] * len(season_years)

for weather in weathersits:
    subset = jumlah_perhari_df[jumlah_perhari_df["weathersit"] == weather]
    penyewaan_values = subset.groupby("season_year")["order_count"].sum().reindex(season_years, fill_value=0)
    
    ax.bar(season_years, penyewaan_values, label=weather, bottom=bottom_values, color=color_palette.get(weather, "#999999"))
    bottom_values += penyewaan_values.values

ax.set_title("Jumlah Penyewaan Berdasarkan Musim, Tahun, dan Kondisi Cuaca", fontsize=14)
ax.set_xlabel("Musim dan Tahun")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xticks(range(len(season_years)))
ax.set_xticklabels(season_years, rotation=45)
ax.legend(title="Kondisi Cuaca")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023')
