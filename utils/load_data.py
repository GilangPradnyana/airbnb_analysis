# utils/load_data.py
import pandas as pd
import os
import requests
from tqdm import tqdm

def download_from_drive():
    url = "https://drive.google.com/uc?export=download&id=1KvwjUQMBMPpjg98Spv1Vual1hXYaPzXL"
    file_path = "data/reviews.csv"
    
    print("📥 Mengunduh file reviews.csv dari Google Drive (±102 MB)...")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(file_path, "wb") as f, tqdm(
        desc="Downloading",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = f.write(chunk)
            bar.update(size)
    
    print(f"✅ File berhasil diunduh! Ukuran: {os.path.getsize(file_path)/1024/1024:.2f} MB")

def load_airbnb_reviews():
    file_path = 'data/reviews.csv'
    
    # Download jika belum ada
    if not os.path.exists(file_path):
        os.makedirs('data', exist_ok=True)
        download_from_drive()
    
    print("📂 Membaca file reviews.csv ...")
    
    # Cek apakah file valid (bukan HTML)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline()
        if '<html' in first_line.lower() or 'google' in first_line.lower():
            raise ValueError("❌ File yang di-download adalah halaman HTML, bukan CSV. Silakan download manual dan upload ulang.")
    
    # Baca CSV dengan debugging
    df = pd.read_csv(file_path, low_memory=False)
    
    print(f"✅ Berhasil membaca file dengan {len(df):,} baris")
    print(f"📋 Kolom yang tersedia: {list(df.columns)}")
    
    # Konversi tanggal (fleksibel)
    date_col = None
    for col in ['date', 'Date', 'DATE']:
        if col in df.columns:
            date_col = col
            break
    
    if date_col:
        df['date'] = pd.to_datetime(df[date_col], errors='coerce')
        print(f"✅ Kolom tanggal ditemukan: '{date_col}'")
    else:
        print("⚠️ Kolom tanggal tidak ditemukan!")
    
    # Tambah kolom analisis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    
    print(f"✅ Total review: {len(df):,}")
    print(f"✅ Listing unik: {df['listing_id'].nunique():,}")
    
    return df