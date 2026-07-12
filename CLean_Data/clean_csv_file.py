
input_file = 'tsukiyo_gacha_revenue_2026-06.csv'
output_file = 'tsukiyo_gacha_revenue_clean.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
    open(output_file, 'w', encoding='utf=8', newline='') as outfile:
        for line in infile:
            clean_line = line.rstrip().rstrip(';')
            
            outfile.write(clean_line + '\n')
            
print("file telah bersih dan rapi wak!", output_file)
        
