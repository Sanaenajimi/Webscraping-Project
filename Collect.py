import os
import requests 
import time
import re

# 1. Récupération du HTML de la page principale
url = 'https://www.europarl.europa.eu/meps/fr/full-list/all'
my_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0'}
response = requests.get(url, headers=my_header)
html_content = response.text

# 2. Création du dossier + sauvegarde du HTML
folder = 'Deputies_page'
file_name = 'Home_page.html'
os.makedirs(folder, exist_ok=True)
file_path = os.path.join(folder, file_name)

# Écriture du HTML dans le fichier
with open(file_path, 'w', encoding='utf-8') as output:
    output.write(html_content)

print(f" HTML de {url} sauvegardé dans {file_path}")

# 3. Lecture du contenu HTML depuis le fichier
with open(file_path, 'r', encoding='utf-8') as f:
    contenu = f.read()

# 4. Extraction des liens des 150 premiers députés
pattern = r'<a href="https://www.europarl.europa.eu/meps/fr/(.*?)" itemprop="url" class="erpl_member-list-item-content mb-3 t-y-block">'
result = re.findall(pattern, contenu)

for n, ele in enumerate(result):
    if n == 150:
        break
    else:
        
        path_folder = os.path.join(folder, ele)
        os.makedirs(path_folder, exist_ok=True)

        deputy_url = f'https://www.europarl.europa.eu/meps/fr/{ele}'
        try:
            req = requests.get(deputy_url, headers=my_header, timeout=10) #recupérer l'url
            deputy_content = req.text #pour avoir le text html , si on a un pdf on fait req.content

            path_file = os.path.join(folder, ele, "page.html")
            with open(path_file, 'w', encoding='utf-8') as output:
                output.write(deputy_content)

        except requests.exceptions.RequestException as e:
            print(f" Erreur lors de la récupération de {deputy_url} : {e}")
            continue

        time.sleep(0.1)
