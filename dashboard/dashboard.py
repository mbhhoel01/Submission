import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn
sns.set(style='dark')

# Helper functions
def create_daily_pm25_df(df):
    daily_pm25_df = df.resample(rule='D', on='datetime').agg({
        "PM2.5": "mean"
    })
    daily_pm25_df = daily_pm25_df.reset_index()
    daily_pm25_df.rename(columns={"PM2.5": "average_pm25"}, inplace=True)
    return daily_pm25_df

def create_monthly_pm25_df(df):
    monthly_pm25_df = df.groupby(df['datetime'].dt.month)['PM2.5'].mean().reset_index()
    monthly_pm25_df.rename(columns={'PM2.5': 'average_pm25', 'datetime': 'month'}, inplace=True)
    return monthly_pm25_df

def create_wind_pm25_correlation(df):
    correlation = df[['WSPM', 'PM2.5']].corr().iloc[0, 1]
    return correlation

# Load cleaned data
air_quality_df = pd.read_csv("main_data.csv")
air_quality_df['datetime'] = pd.to_datetime(air_quality_df['datetime'])

# Filter data
min_date = air_quality_df['datetime'].min()
max_date = air_quality_df['datetime'].max()

with st.sidebar:
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date = st.date_input(
        label='Tanggal Mulai',
        value=min_date
    )
    end_date = st.date_input(
        label='Tanggal Selesai',
        value=max_date
    )

main_df = air_quality_df[(air_quality_df['datetime'] >= str(start_date)) & 
                          (air_quality_df['datetime'] <= str(end_date))]

# Prepare dataframes
daily_pm25_df = create_daily_pm25_df(main_df)
monthly_pm25_df = create_monthly_pm25_df(main_df)
wind_pm25_correlation = create_wind_pm25_correlation(main_df)

# Dashboard Title
st.header('Dashboard Kualitas Udara di Distrik Aotizhongxin Beijing :sparkles:')

# Daily PM2.5 Orders
st.subheader('Rata-rata PM2.5 Harian')

col1, col2 = st.columns(2)

with col1:
    total_days = daily_pm25_df.shape[0]
    st.metric("Total Hari", value=total_days)

with col2:
    avg_pm25 = round(daily_pm25_df['average_pm25'].mean(), 2)
    st.metric("Rata-rata PM2.5", value=avg_pm25)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_pm25_df["datetime"],
    daily_pm25_df["average_pm25"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Monthly PM2.5 Performance
st.subheader("Rata-rata PM2.5 Bulanan")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="month", 
    y="average_pm25", 
    data=monthly_pm25_df,
    palette="coolwarm",
    ax=ax
)
ax.set_title("Rata-rata PM2.5 per Bulan", loc="center", fontsize=50)
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)", fontsize=30)
ax.set_xlabel("Bulan", fontsize=30)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Wind and PM2.5 Correlation
st.subheader("Korelasi antara Kecepatan Angin dan PM2.5")

st.write(f"Korelasi antara kecepatan angin dan PM2.5 adalah: {round(wind_pm25_correlation, 2)}")

# Conclusion
st.header("Kesimpulan")
st.write("""
1. Rata-rata PM2.5 menunjukkan fluktuasi yang signifikan selama periode yang dianalisis.
2. Bulan-bulan dengan curah hujan yang lebih tinggi cenderung menunjukkan tingkat PM2.5 yang lebih rendah.
3. Terdapat korelasi negatif antara kecepatan angin dan tingkat PM2.5, yang menunjukkan bahwa kecepatan angin yang lebih tinggi dapat membantu mengurangi polusi udara.
""")

st.caption('Copyright © Hoel.id 2025')