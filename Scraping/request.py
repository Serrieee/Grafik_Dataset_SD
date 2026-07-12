
import pandas as pd
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

hasil_semua_game = []

# --- FUNGSI PELACAK HARTA KARUN (REKURSIF) ---
# Fungsi ini akan membongkar JSON sedalam apa pun untuk mencari data revenue
def cari_data_revenue(data_json, target_year=2026):
    hasil_ditemukan = []
    
    if isinstance(data_json, list):
        for item in data_json:
            if isinstance(item, dict) and ('revenue' in item or 'value' in item) and 'month' in item and 'year' in item:
                # BINGO! Kita menemukan struktur datanya
                if item.get("year") == target_year and item.get("month") in [1, 2, 3, 4, 5, 6]:
                    hasil_ditemukan.append(item)
            else:
                # Kalau bukan, gali lebih dalam lagi
                hasil_ditemukan.extend(cari_data_revenue(item, target_year))
                
    elif isinstance(data_json, dict):
        for key, val in data_json.items():
            hasil_ditemukan.extend(cari_data_revenue(val, target_year))
            
    return hasil_ditemukan

print("Menginisialisasi Browser Edge (Jurus Terminator V6)...")
options = webdriver.EdgeOptions()
# options.add_argument('--headless') # Biarkan mati dulu
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

try:
    # 1. Buka halaman utama
    driver.get("https://revenue.ennead.cc/revenue")
    print("Menunggu halaman dan tabel dimuat (Melewati Cloudflare)...")
    
    # Tunggu sampai tabel utama muncul di layar
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    time.sleep(3)
    
    baris_tabel = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    total_baris = len(baris_tabel)
    print(f"Berhasil menemukan {total_baris} baris data di halaman ini!")
    
    # --- SUNTIKAN SCRIPT PENYADAP (HACKER MODE V6: SADAP SEMUANYA) ---
    interceptor_script = """
    window.hasilScraping = { allData: [], logUrl: [] };
    
    // Sadap Fetch API
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        let url = (args[0] && typeof args[0] === 'string') ? args[0] : (args[0] && args[0].url ? args[0].url : 'unknown_url');
        window.hasilScraping.logUrl.push('FETCH: ' + url);
        
        let promise = originalFetch.apply(this, args);
        promise.then(response => {
            const clone = response.clone();
            clone.text().then(text => {
                try {
                    let json = JSON.parse(text);
                    // Simpan URL beserta isi JSON-nya
                    window.hasilScraping.allData.push({ url: url, data: json });
                } catch(e) {} // Abaikan jika bukan JSON (misal gambar/html)
            }).catch(e => {});
        }).catch(e => {});
        return promise;
    };

    // Sadap XHR
    const XHR = XMLHttpRequest.prototype;
    const open = XHR.open;
    const send = XHR.send;
    XHR.open = function(method, url) {
        this._url = url;
        window.hasilScraping.logUrl.push('XHR: ' + url);
        return open.apply(this, arguments);
    };
    XHR.send = function() {
        this.addEventListener('load', function() {
            try { 
                let json = JSON.parse(this.responseText);
                window.hasilScraping.allData.push({ url: this._url, data: json });
            } catch(e) {}
        });
        return send.apply(this, arguments);
    };
    """
    driver.execute_script(interceptor_script)
    print("Sistem penyadap jaringan (Mode Terminator V6) berhasil dipasang!\n")

    # 3. Mulai proses otomatisasi
    for i in range(min(5, total_baris)): 
        
        try:
            baris_sekarang = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")[i]
            
            # --- MENCARI NAMA GAME ---
            kolom_kolom = baris_sekarang.find_elements(By.TAG_NAME, "td")
            nama_game = None
            elemen_klik = None
            
            for col in kolom_kolom:
                teks = col.text.strip()
                if re.search(r'[a-zA-Z]', teks):
                    nama_game = teks.split('\n')[0]
                    elemen_klik = col
                    break
            
            if not nama_game:
                continue
                    
            print(f"-> Memproses: {nama_game}")
            
            # KOSONGKAN BRANKAS
            driver.execute_script("window.hasilScraping.allData = []; window.hasilScraping.logUrl = [];")
            
            # Fokus ke elemen TANPA scroll offset yang bikin meleset
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", baris_sekarang)
            time.sleep(1)
            
            # --- JURUS KLIK 3 LAPIS (PASTI KENA) ---
            driver.execute_script("arguments[0].click();", elemen_klik) # Klik sel-nya
            driver.execute_script("arguments[0].click();", baris_sekarang) # Klik barisnya
            
            # Coba cari link (<a>) di dalam sel dan klik juga
            try:
                link = elemen_klik.find_element(By.TAG_NAME, "a")
                driver.execute_script("arguments[0].click();", link)
            except: pass
            
            # Tunggu 6 detik agar grafik dan API benar-benar selesai loading
            time.sleep(6) 
            
            # AMBIL SEMUA DATA
            kumpulan_data_tersadap = driver.execute_script("return window.hasilScraping['allData'];")
            log_url = driver.execute_script("return window.hasilScraping['logUrl'];")
            
            berhasil_ekstrak = False
            
            if kumpulan_data_tersadap:
                # Periksa setiap respons jaringan yang ditangkap
                for paket in kumpulan_data_tersadap:
                    url_sumber = paket.get('url', '')
                    data_json = paket.get('data', {})
                    
                    # Gunakan fungsi pelacak kita untuk mencari data revenue
                    data_bersih = cari_data_revenue(data_json, target_year=2026)
                    
                    if data_bersih:
                        for item in data_bersih:
                            hasil_semua_game.append({
                                "Game": nama_game,
                                "Tahun": item.get("year"),
                                "Bulan (Angka)": item.get("month"),
                                "Region": item.get("region", "GLOBAL"),
                                "Revenue (USD)": item.get("revenue", item.get("value"))
                            })
                        berhasil_ekstrak = True
                        print(f"   [OK] Data ditemukan dari URL: {url_sumber.split('/')[-1][:20]}...")
                        break # Berhenti mencari di paket lain jika sudah ketemu
            
            if not berhasil_ekstrak:
                print("   [GAGAL] Tidak ada data revenue 2026 di dalam JSON yang ditangkap.")
                print(f"   [DEBUG NETWORK LOG]: {log_url if log_url else 'Kosong (Klik gagal/Grafik tidak muncul)'}")
                
        except Exception as e:
            print(f"   [ERROR] Gagal saat memproses baris: {e}")

finally:
    driver.quit()

# 4. Simpan hasilnya ke CSV baru
if hasil_semua_game:
    df_hasil = pd.DataFrame(hasil_semua_game)
    df_hasil.to_csv("tsukiyo_gacha_revenue_new.csv", index=False)
    print("\nPROSES SELESAI! Data berhasil disimpan di 'tsukiyo_gacha_revenue_new.csv'")
else:
    print("\ntidak ada data yang di extrak")
        