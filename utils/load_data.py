# utils/load_data.py
import pandas as pd
import os

def load_airbnb_reviews():
    file_path = 'data/reviews.csv'
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File {file_path} tidak ditemukan! Pastikan reviews.csv sudah ada di folder data/")
    
    print("📂 Sedang memuat reviews.csv (bisa agak lama karena file besar)...")
    
    # Baca file baru dengan benar
    df = pd.read_csv(file_path, 
                     parse_dates=['date'], 
                     low_memory=False)
    
    # Tambah kolom analisis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    
    print(f"✅ Berhasil memuat {len(df):,} review dari {df['listing_id'].nunique():,} listing!")
    print(f"   Kolom yang tersedia: {list(df.columns)}")
    
    return df