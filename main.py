
import pandas as pd
import matplotlib.pyplot as plt
from utils import muat_dan_siapkan_data

def main():
    print("Data Gacha Revenue......")
   
    # Pastikan file CSV ada di dalam folder 'dataset'
    df_game, kolom_bulan = muat_dan_siapkan_data('Dataset/tsukiyo_gacha_revenue.csv')

    # Perhitungan Statistik Deskriptif seperti sorting dan lain lain
    game_tertinggi = df_game["total_pendapatan"].max() # Baris pertama setelah di-sort
    game_terendah = df_game["total_pendapatan"].min()
    rata_rata_6bulan = df_game['total_pendapatan'].mean()
    
    game_revenue_high = df_game[df_game["total_pendapatan"] == game_tertinggi].iloc[0]["game"]
    game_revenue_low = df_game[df_game["total_pendapatan"] == game_terendah].iloc[0]["game"]

    # Menulis Hasil ke File ke hasil_analisis.txt
    with open('hasil_analisis.txt', 'w') as file:
        file.write("================================================\n")
        file.write(" RINGKASAN PENDAPATAN TOP 12 MOBILE GAME GACHA 2026\n")
        file.write("================================================\n\n")
        
        file.write(f"Game dengan Pendapatan Total Tertinggi (Jan-Jun):\n")
        file.write(f"- Nama Game: {game_revenue_high}\n")
        # Dibagi 1 atau 1e6 juta karena hitunganya per million dollar
        file.write(f"- Total Pendapatan: ${game_tertinggi / 1e6:.2f} Juta USD\n\n")
        
        file.write(f"Game Dengan Pendapatan Ternedah Diantara 12 Game Lain:\n")
        file.write(f"- Nama Game: {game_revenue_low}\n")
        file.write(f"- Pendaptan: ${game_terendah / 1e6:.2f} Juta USD\n\n")
        
        file.write(f"Rata-rata pendapatan dari Top 12 Game selama 6 bulan adalah:\n")
        file.write(f"- Pendapatan Rata-Rata: ${rata_rata_6bulan / 1e6:.2f} Juta USD\n")

    print("File 'hasil_analisis.txt' berhasil dibuat!")

    # 4. Membuat 2 Visualisasi Grafik dalam 1 Gambar (Subplots)
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

    # --- GRAFIK ATAS: Bar Plot (Total Pendapatan) ---
    axes[0].bar(df_game['game'], df_game['total_pendapatan'] / 1e6, color='#2ecc71', edgecolor='black')
    axes[0].set_title('Top 10 Mobile Gacha Game Revenue (Januari - Juni 2026)', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Total Pendapatan (Juta USD)', fontsize=12)

    # PERBAIKAN 1: Miringkan 45 derajat dan jangkar teks di sebelah kanan (ha='right')
    axes[0].set_xticks(range(len(df_game['game'])))
    axes[0].set_xticklabels(df_game['game'], rotation=45, ha='right')

    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # --- GRAFIK BAWAH: Line Plot (Tren Bulanan) ---
    label_bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun']

    for indeks, baris in df_game.iterrows():
        axes[1].plot(label_bulan, baris[kolom_bulan] / 1e6, marker='o', linewidth=2, label=baris['game'])

    axes[1].set_title('Pendapatan Bulanan', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Pendapatan per Bulan (Juta USD)', fontsize=12)
    axes[1].set_xlabel('Bulan (2026)', fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)

    # PERBAIKAN 2: Tambahkan h_pad (Horizontal Padding) agar jarak atas-bawah renggang
    plt.tight_layout(h_pad=3.0)

    # Simpan Grafik ke PNG
    plt.savefig('grafik_output.png', dpi=150, bbox_inches='tight')
    print("Grafik berhasil disimpan sebagai 'grafik_output.png'!")
    
    plt.show()

   
if __name__ == "__main__":
    main()
    
