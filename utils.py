
import pandas as pd
import re

def muat_dan_siapkan_data(filepath):
    df = pd.read_csv(filepath)
    
    kolom_bulan = [
        "january_2026_usd", "february_2026_usd", "march_2026_usd",
        "april_2026_usd", "may_2026_usd", "june_2026_usd"
    ]
    
    df_bersih = df.dropna(subset=kolom_bulan).copy()
    
    df_bersih["total_pendapatan"] = df_bersih[kolom_bulan].sum(axis=1)
    
    df_top15 = df_bersih.sort_values(by="total_pendapatan", ascending=False).head(12)
    
    return df_top15, kolom_bulan
    
    