
import re
import requests
import pdb

for folder in os.listdir('Deputies_page'):
    folder_path = os.path.join('Deputies_page', folder)
    deputy_file_path = os.path.join(folder_path, 'report.html')
    if os.path.exists(deputy_file_path):
        with open(deputy_file_path, 'r', encoding='utf-8') as output:
            deputy_content = output.read()
            
        pattern_pdf = r'https://www.europarl.europa.eu/doceo/document/[^"]+\.pdf'
        result_pdf = re.findall(pattern_pdf,deputy_content)
        print(folder,len(result_pdf))
        for k,pdf_url in enumerate(result_pdf): 
            pdf_path = os.path.join(folder_path, 'Rapport_principal_{}.pdf'.format(k))
            response = requests.get(pdf_url)
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f" Téléchargé : {folder}")
