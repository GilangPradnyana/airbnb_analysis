# utils/load_data.py
import pandas as pd
import os
import requests
from tqdm import tqdm

def download_from_drive():
    url = "https://drive.google.com/uc?export=download&id=1KvwjUQMBMPpjg98Spv1Vual1hXYaPzXL"
    file_path = "data/reviews.csv"
    
    print("📥 Mengunduh file reviews.csv dari Google Drive (sekitar 102 MB)...")
    
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
    
    print("✅ File berhasil diunduh!")

def load_airbnb_reviews():
    file_path = 'data/reviews.csv'
    
    # Jika file belum ada, download dulu
    if not os.path.exists(file_path):
        os.makedirs('data', exist_ok=True)
        download_from_drive()
    
    print("📂 Memuat dataset reviews.csv ...")
    
    df = pd.read_csv(file_path, parse_dates=['date'], low_memory=False)
    
    # Tambah kolom analisis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    
    print(f"✅ Berhasil memuat {len(df):,} review dari {df['listing_id'].nunique():,} listing!")
    
    return df