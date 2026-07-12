
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

#crhome sbagai akses ke web drivernya
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://tsukiyo.gg/"

try:
    print("buka website....")
    driver.get(url)
    
    #list menampung bulanya wak
    all_months_data = []
    
    #rentang bulan
    target_months = ["january 2026", "february 2026", "march 2026", "april 2026", "may 2026", "june 2026"]
    
    for months in target_months:
        print(f"\nMemproses data untuk bulan{months}")
        
        #filteriing
        try:
            month_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID))
            )
            month_dropdown.click()
            time.sleep(1)
            
            #target bulan
            target_option = driver.find_element(By.XPATH, f"//option[text()='{months}']")
            target_option.click()
            
            print(f"filter behasil di ubah ke {months}. Menunggu tabel memuat data ....")
        except:
            print(f"filter bulan {months} tidak ditemuakn")
            
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )    
        time.sleep(2)
        
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 4:
                rank = columns[0].text.strip()
                game = columns[1].text.strip()
                regions = columns[2].text.strip()
                revenue = columns[3].text.strip()
                
                all_months_data.append({
                    "Bulan": months,
                    "Rank": rank,
                    "Game": game,
                    "Regions": regions,
                    "Revenue (USD)": revenue
                })
        print(f"BErhasil mengestrak {len(rows)} game untuk bulan {months}")
        
    #simapn hasil ahir ke dataframe dengan format csv
    df = pd.DataFrame(all_months_data)
    df.to_csv("tsukiyo_revenue.csv", index=False, encoding="utf-8")
    print("\nProses selsai, data di simpan di file tsukiyo_revenue.csv")            
                        
finally:
    #hapus dari ram
    driver.quit()
    
        
    

