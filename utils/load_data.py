# utils/load_data.py
import pandas as pd
import os
import requests
from tqdm import tqdm

def download_from_drive():
    file_id = "1KvwjUQMBMPpjg98Spv1Vual1hXYaPzXL"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    file_path = "data/reviews.csv"
    
    print("📥 Mengunduh file reviews.csv dari Google Drive (±102 MB)...")
    
    session = requests.Session()
    
    # Langkah 1: Dapatkan response awal
    response = session.get(url, stream=True)
    
    # Langkah 2: Tangani konfirmasi Google Drive untuk file besar
    confirm_token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            confirm_token = value
            break
    
    if confirm_token:
        url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}"
        response = session.get(url, stream=True)
    
    # Download dengan progress bar
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
    
    # Download jika file belum ada
    if not os.path.exists(file_path):
        os.makedirs('data', exist_ok=True)
        download_from_drive()
    
    print("📂 Membaca file reviews.csv ...")
    
    # Baca CSV
    df = pd.read_csv(file_path, low_memory=False)
    
    print(f"✅ Berhasil membaca {len(df):,} baris data")
    print(f"📋 Kolom yang tersedia: {list(df.columns)}")
    
    # Konversi tanggal
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    else:
        print("⚠️ Kolom 'date' tidak ditemukan!")
    
    # Tambah kolom analisis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    
    return df