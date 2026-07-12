
import pandas as pd

dataframe = pd.read_csv("tsukiyo_gacha_revenue_clean.csv")

exel_file = "tsukiyo_gacha_revenue.xlsx"
dataframe.to_excel(exel_file, index=False)

print(f"simpan ke {exel_file}")
