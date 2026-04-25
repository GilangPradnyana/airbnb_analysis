# utils/load_data.py
import pandas as pd
import os

def load_airbnb_reviews():
    file_path = 'data/reviews.csv'
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File {file_path} tidak ditemukan!\n"
                              f"Pastikan file reviews.csv sudah ada di folder data/")
    
    print("📂 Membaca file reviews.csv (gzip compressed) ...")
    
    # ← INI YANG BARU: pakai compression='gzip'
    df = pd.read_csv(file_path, compression='gzip', low_memory=False)
    
    print(f"✅ Berhasil membaca {len(df):,} baris data")
    print(f"📋 Kolom yang tersedia: {list(df.columns)}")
    
    # Konversi tanggal
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        print("✅ Kolom 'date' berhasil dikonversi")
    else:
        print("⚠️ Kolom 'date' tidak ditemukan!")
    
    # Tambah kolom analisis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    
    print(f"✅ Total review: {len(df):,}")
    print(f"✅ Listing unik: {df['listing_id'].nunique():,}")
    
    return df