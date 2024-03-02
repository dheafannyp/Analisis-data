import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')
st.set_page_config(
        page_title="Analisis Data",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )
# Load data
day_df = pd.read_csv("day.csv")

# Menghapus kolom yang tidak diperlukan
drop_cols = ['instant', 'dteday', 'windspeed']
day_df.drop(columns=drop_cols, inplace=True)

# Mengubah nama kolom
day_df.rename(columns={
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_condition',
    'cnt': 'total_count'
}, inplace=True)

# Mengubah angka menjadi keterangan
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_condition'] = day_df['weather_condition'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Sidebar
with st.sidebar:
    st.title('Bike Sharing Dashboard')
    st.text('by Dhea Fanny Putri Syarifa')
    st.image('bike.jpg')

    # Sidebar dengan dropdown untuk memilih jenis pengguna
    user_type = st.sidebar.selectbox("Pilih jenis pengguna:", ("Semua Jenis Pengguna", "Casual", "Registered"))

# main page
st.title(f'Analisis Bike Sharing Tahun {user_type}')

if user_type == 'Casual':
    st.write("Ini adalah tampilan khusus untuk pengguna Casual.")
    casual_user = day_df['casual'].sum()
    st.write("Casual User:", casual_user)
    monthly_casual_user = day_df.groupby('month')['casual'].sum().reset_index()

    # Menampilkan grafik menggunakan streamlit
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_casual_user, x='month', y='casual', marker='o', ax=ax)
    ax.set_title('Tren Jumlah Pengguna Casual Sepeda per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pengguna Casual')
    ax.set_xticks(monthly_casual_user['month'])
    ax.grid(True)
    plt.tight_layout()

    st.pyplot(fig)
    st.title("Analisis Hari Kerja Paling Banyak Digunakan oleh Pengguna Casual")

    # Hitung jumlah pengguna casual yang menggunakan sepeda pada setiap hari kerja
    casual_weekday_count = day_df.groupby('weekday')['casual'].sum().reset_index()

    # Membuat grafik menggunakan seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=casual_weekday_count, x='weekday', y='casual')
    plt.title('Jumlah Pengguna Casual yang Menggunakan Sepeda pada Setiap Hari Kerja')
    plt.xlabel('Hari Kerja')
    plt.ylabel('Jumlah Pengguna Casual')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Menampilkan grafik menggunakan Streamlit
    st.pyplot(plt)
    
elif user_type == 'Registered':
    st.write("Ini adalah tampilan khusus untuk pengguna Registered.")
    # Menghitung jumlah total pengguna terdaftar per bulan
    monthly_registered_user = day_df.groupby('month')['registered'].sum().reset_index()

    # Menampilkan grafik menggunakan streamlit
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_registered_user, x='month', y='registered', marker='o', ax=ax)
    ax.set_title('Tren Jumlah Pengguna Registered Sepeda per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pengguna Registered')
    ax.set_xticks(monthly_registered_user['month'])
    ax.grid(True)
    plt.tight_layout()

    st.pyplot(fig)

    st.title("Analisis Hari Kerja Paling Banyak Digunakan oleh Pengguna Terdaftar")

    # Hitung jumlah pengguna terdaftar yang menggunakan sepeda pada setiap hari kerja
    registered_weekday_count = day_df.groupby('weekday')['registered'].sum().reset_index()

    # Membuat grafik menggunakan seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=registered_weekday_count, x='weekday', y='registered')
    plt.title('Jumlah Pengguna Terdaftar yang Menggunakan Sepeda pada Setiap Hari Kerja')
    plt.xlabel('Hari Kerja')
    plt.ylabel('Jumlah Pengguna Terdaftar')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Menampilkan grafik menggunakan Streamlit
    st.pyplot(plt)

else:
    # Menghitung total user, casual user, dan registered user
    total_user = day_df['total_count'].sum()
    casual_user = day_df['casual'].sum()
    registered_user = day_df['registered'].sum()
    # Menampilkan informasi dalam bentuk kolom
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Total User:", total_user)

    with col2:
        st.write("Casual User:", casual_user)

    with col3:
        st.write("Registered User:", registered_user)
    
    # Grafik jumlah total user per bulan
    monthly_total_user = day_df.groupby('month')['total_count'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=monthly_total_user, x='month', y='total_count', ax=ax)
    ax.set_title('Jumlah Total User per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Total User')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

    with tab1:
        st.title("Tren Penggunaan Sepeda Sepanjang Tahun")
        # Hitung jumlah total penggunaan sepeda pada setiap bulan
        monthly_total_count = day_df.groupby('month')['total_count'].sum().reset_index()

        # Membuat grafik menggunakan seaborn
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=monthly_total_count, x='month', y='total_count', marker='o')
        plt.title('Tren Penggunaan Sepeda Sepanjang Tahun')
        plt.xlabel('Bulan')
        plt.ylabel('Total Penggunaan Sepeda')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Menampilkan grafik menggunakan Streamlit
        st.pyplot(plt)
        
    with tab2:
        # Menyiapkan data untuk digunakan pada grafik
        season_weekday_count = day_df.groupby(['season', 'weekday'])['total_count'].mean().reset_index()

        # Membuat grafik menggunakan seaborn
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=season_weekday_count, x='weekday', y='total_count', hue='season', marker='o')
        plt.title('Hubungan Musim dengan Jumlah Sewa berdasarkan Hari Kerja')
        plt.xlabel('Hari Kerja')
        plt.ylabel('Jumlah Sewa Rata-rata')
        plt.xticks(rotation=45)
        plt.legend(title='Musim')
        plt.grid(True)

        # Menampilkan grafik menggunakan Streamlit
        st.pyplot(plt)

    
    with tab3:
        st.title("Analisis Jumlah Sewa Berdasarkan Kondisi Cuaca")

        # Menghitung rata-rata jumlah sepeda yang dipinjam berdasarkan kondisi cuaca
        weather_avg_count = day_df.groupby('weather_condition')['total_count'].mean().reset_index()

        # Membuat grafik menggunakan seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(data=weather_avg_count, x='weather_condition', y='total_count')
        plt.title('Rata-rata Jumlah Sepeda yang Dipinjam Berdasarkan Kondisi Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Jumlah Sepeda Dipinjam')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Menampilkan grafik menggunakan Streamlit
        st.pyplot(plt)


    


st.caption('Copyright © Dhea Fanny Putri Syarifa 2024')
