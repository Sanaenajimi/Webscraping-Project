import os
import re
import requests
import pdb
import pandas as pd

liste_generale = []
# Parcourir les dossiers des députés et extraire les informations
for folder in os.listdir('Deputies_page'):
    folder_path = os.path.join('Deputies_page', folder)
    
    # Vérifier si c'est un dossier (c'est-à-dire une page pour un député)
    if os.path.isdir(folder_path):
        print(f"id : {folder}...")

        # Construction du chemin vers le fichier HTML du député
        deputy_file_path = os.path.join(folder_path, 'page.html')

        # Lecture du  contenu de la page HTML du député
        with open(deputy_file_path, 'r', encoding='utf-8') as output:
            deputy_content = output.read()
            
        #pdb.set_trace() : comment for now but to verify type it without #
        
        # extraire les informations du député
        
        pattern_name = r'<a id="mep-mp3" class="erpl_mep-mp3" title="(.*?)"></a>'
        pattern_job_France = r'<h3 class="erpl_title-h3 mt-1 sln-political-group-name">(.*?)</h3>'
        pattern_job_Intern = r'<div class="erpl_title-h3 mt-1 mb-1">\s*([^<\n]+)\s*-\s*([^<\n]+)\s*</div>'
        pattern_birthday = r'<p >Date de naissance  : <time class="sln-birth-date" datetime="(.*?)">'
        pattern_email = r'<a class="link_email.*?".*?href="(.*?)"' #Là on se rend compte que mr-2 existe dans qlq fichiers et pas dans autres
        #donc on va la remplacer par {0: càd aucun caractère comme pour le cas 2, à 4 caract : mr-2}, là pas de parenthèses , il faut que le programme parcour seulement et ne capte pas l'info
        pattern_twitter = r'<a class="twitter" title="Partager cette page sur X".*?href="(.*?)" target="_blank">'
        
        name = re.findall(pattern_name, deputy_content)
        job_France = re.findall(pattern_job_France, deputy_content)
        job_Intern = re.findall(pattern_job_Intern, deputy_content)
        birth_day = re.findall(pattern_birthday, deputy_content)
        mail = re.findall(pattern_email,deputy_content)
        twitter = re.findall(pattern_twitter,deputy_content)

        # Traitement des résultats :
        if len(job_France) == 1:
            job_France = job_France[0]
        else:
            job_France = "" 
        if len(job_Intern) == 1:
            job_Intern = job_Intern[0]
        else:
            job_Intern = ""

        if len(birth_day) >= 1:
            birth_day = birth_day[0]
        else:
            birth_day = ""
        
        if len(mail) >= 1:
            raw_mail = mail[0]
            mail = raw_mail.replace('[dot]', '.').replace('[at]', '@')[::-1]
            m = ''
            for e in mail :
                m = e + m 
            mail_new = m
            print(mail_new)
        else:
            print("")
        
        if len(twitter) >= 1:
            twitter = twitter[0]
        else :
            print("")
    
        # Affichage des résultats pour chaque député
        print(f"Député: {name}")
        print(f"Fonction en France: {job_France}")
        print(f"Fonction à l'international: {job_Intern}")
        print(f"Date de naissance: {birth_day}")
        print(f"Mail:  {mail}")
        print(f"Twitter : {twitter}")
        liste_deputy = [folder,name,job_France,job_Intern,birth_day,mail,twitter]
        print(liste_deputy)
        print('-------------------')
        
        #Création d'une liste des infos 
        liste_generale.append(liste_deputy)
print(liste_generale)

#Création d'une data frame 
col_header = ["ID", "Nom", "Fonction_France", "Fonction_International", "Date_de_naissance", "Email", "Twitter"]

df = pd.DataFrame(liste_generale, columns=col_header)
print(df)
df.to_excel('test.xlsx')

