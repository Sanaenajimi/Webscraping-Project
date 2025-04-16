s
import re
import pdb
import requests

# Define the base directory containing the deputies' pages
base_dir = 'Deputies_page'

# Step 1: Read the source code of each deputy's page
for folder in os.listdir(base_dir):
    if folder !='Home_page.html':  #comme home_page n'est pas un folder ça va renvoyer une erreur
        folder_path = os.path.join(base_dir, folder)
        deputy_file_path = os.path.join(folder_path, 'page.html')
        with open(deputy_file_path, 'r', encoding='utf-8') as output:
            deputy_content = output.read()

        # Step 2: Check if the report exists in each page

        if deputy_content.find('/main-activities/reports#detailedcardmep">')!=-1:
            pattern_report = '/meps/fr/(.*?)/main-activities/reports#detailedcardmep">'       
            Result = re.findall(pattern_report,deputy_content)
            deputy_url_report = 'https://www.europarl.europa.eu/meps/fr/{}/main-activities/reports#detailedcardmep">'.format(Result[0])
            
            header_report = {'User_Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0}'}  
            req = requests.get(deputy_url_report, headers=header_report, timeout=10) #recupérer l'url
            report_content = req.text #pour avoir le text html , si on a un pdf on fait req.content
            path_file = os.path.join(folder_path, "report.html")
            
            with open(path_file, 'w', encoding='utf-8') as output:
                    output.write(report_content)
            
