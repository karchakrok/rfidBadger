import sqlite3
import datetime
import os

conn = sqlite3.connect('rfid.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS rfid
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               badge_id TEXT,
               porte_id INTEGER, 
               h_entree DATETIME,
               h_sortie DATETIME)''')

def badger_une_carte(badge_id:str, porte_id:int):
        if len(badge_id) != 8: # Vérifie que le numéro de série du badge est bien composé de 8 caractères
                print("Le numéro de série du badge doit être composé de *8 caractères* hexadécimaux") 
        try:
                int(badge_id, 16) # Vérifie que le numéro de série du badge est bien composé de caractères hexadécimaux
        except:
                print("Le numéro de série du badge doit être composés de 8 caractères *héxadécimaux*.")

        h_entree = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") #strftime sert a mettre en forme la donnée enregistré
        h_sortie = (datetime.datetime.strptime(h_entree, "%d/%m/%Y %H:%M:%S") + datetime.timedelta(hours=1)).strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute("INSERT INTO rfid (badge_id, porte_id, h_entree, h_sortie) VALUES (?, ?, ?, ?)", (badge_id, porte_id, h_entree, h_sortie))
        print('Carte badgée avec succès !')
        print(f"Numéro de série du badge : {badge_id}")
        print(f"Numéro de la porte : {porte_id}")
        print(f"Heure d'entrée : {h_entree}")
        print(f"Heure de sortie : {h_sortie}\n")
        conn.commit()
                
def tracer_une_carte(badge_id:str):
        print('''1. Par date prédéfinie (du X au X) \n2. Par ordre chronologique\n''')
        choix = input(f"{underline('menu@rfid:~$')} Entrez votre choix : \n")
        choix = int(choix)
        if choix == 1:
                date_debut = input(f"{underline('menu@rfid:~$')} Entrez la date de début (format : dd/mm/YY) : \n")
                date_fin = input(f"{underline('menu@rfid:~$')} Entrez la date de fin (format : dd/mm/YY) : \n")
                cursor.execute("SELECT * FROM rfid WHERE badge_id = ? AND h_entree BETWEEN ? AND ?", (badge_id, date_debut, date_fin))
                data = (cursor.fetchall())
                print('ID ||   BADGE    ||  PORTE  ||     HEURE ENTREE    ||    HEURE SORTIE')
                print('')
                for i in range(len(data)): # Permet un affichage plus lisible
                        print(f"{data[i][0]}  ||  {data[i][1]}  ||    {data[i][2]}    || {data[i][3]} || {data[i][4]}")
        elif choix == 2:
                cursor.execute("SELECT * FROM rfid WHERE badge_id = ? ORDER BY h_entree", (badge_id,))
                data = (cursor.fetchall())
                print('ID ||   BADGE    ||  PORTE  ||     HEURE ENTREE    ||    HEURE SORTIE')
                print('')
                for i in range(len(data)): # Permet un affichage plus lisible
                        print(f"{data[i][0]}  ||  {data[i][1]}  ||    {data[i][2]}    || {data[i][3]} || {data[i][4]}")
        else:
                print("Choix invalide")

def effacer_une_carte(badge_id:str):
        print('''1. Effacer un badge \n2. Effacer une date''')
        choix = input(f"{underline('menu@rfid:~$')} Entrez votre choix : \n")
        choix = int(choix)
        if choix == 1:
                cursor.execute("DELETE FROM rfid WHERE badge_id = ?", (badge_id,))
                conn.commit()
                print(f"Les entrées du badge {badge_id} ont été effacées avec succès !")
        elif choix == 2:
                date_debut = input(f"{underline('menu@rfid:~$')} Entrez la date de début (format : dd/mm/YY) : \n")
                date_fin = input(f"{underline('menu@rfid:~$')} Entrez la date de fin (format : dd/mm/YY) : \n")
                cursor.execute("DELETE * FROM rfid WHERE h_entree BETWEEN ? AND ?", (date_debut, date_fin))
                print(f"Les entrées enregistrées entre le {date_debut} et le {date_fin} ont été effacées avec succès !")
        else:
                print('Choix invalide')

def ajouter_une_entree(badge_id:str, porte_id:int, h_entree, h_sortie):
        cursor.execute("INSERT INTO rfid (badge_id, porte_id, h_entree, h_sortie) VALUES (?, ?, ?, ?)", (badge_id, porte_id, h_entree, h_sortie))
        conn.commit()
        print("Entrée ajoutée avec succès !")

def corriger_une_entree(badge_id:str, h_entree, h_sortie):
        cursor.execute("UPDATE rfid SET h_entree = ?, h_sortie = ? WHERE badge_id = ?", (h_entree, h_sortie, badge_id))
        conn.commit()
        print("Entrée corrigée avec succès !")

def montrer_toutes_les_entrees():
        cursor.execute("SELECT * FROM rfid")
        data = (cursor.fetchall())
        print('ID ||   BADGE    ||  PORTE  ||     HEURE ENTREE    ||    HEURE SORTIE')
        print('')
        for i in range(len(data)): # Permet un affichage plus lisible
                print(f"{data[i][0]}  ||  {data[i][1]}  ||    {data[i][2]}    || {data[i][3]} || {data[i][4]}")
        print('')


def underline(text:str):
        return '\033[4m' + text + '\033[0m' # Sert à souligner le texte pour l'esthétique


var = "clear"

while True:
        os.system(var)
        print("""                                  
`88.       .888                                   
888b     d'888   .ooooo.  ooo. .oo.   oooo  oooo  
8 Y88. .P  888  d88' `88b `888P"Y88b  `888  `888  
8  `888'   888  888ooo888  888   888   888   888   
8    Y     888  888    .o  888   888   888   888  
o8o        o888o `Y8bod8P' o888o o888o  `V88V"V8P

1. Badger une carte
2. Tracer une carte
3. Effacer une entrée
4. Ajouter une entrée manuellement
5. Corrigez une date déjà enregistrée
6. Montrer toutes les entrées
7. Quitter le menu
        """) # https://edukits.co/text-art/

        menu_selection = input(f"{underline('menu@rfid:~$')} Entrez votre choix : \n")
        try:
                menu_selection = int(menu_selection)
        except: # Si l'utilisateur lance le programme alors qu'il est déjà lancé, ca relance sans faire d'erreurs
                var = menu_selection 
                break 

        if menu_selection == 1:
                badge = input(f"{underline('menu@rfid:~$')} Entrez le numéro de série du badge : \n").upper()
                porte = input(f"{underline('menu@rfid:~$')} Entrez le numéro de la porte : \n")
                badger_une_carte(badge, porte)

        elif menu_selection == 2:
                badge = input(f"{underline('menu@rfid:~$')} Entrez le numéro de série du badge : \n").upper() # .upper() sert à mettre en majuscule
                tracer_une_carte(badge)

        elif menu_selection == 3:
                badge = input(f"{underline('menu@rfid:~$')} Entrez le numéro de série du badge : \n").upper()
                effacer_une_carte(badge)

        elif menu_selection == 4:
                badge = input(f"{underline('menu@rfid:~$')} Entrez le numéro de série du badge : \n").upper()
                porte = input(f"{underline('menu@rfid:~$')} Entrez le numéro de la porte : \n")
                h_entree = input(f"{underline('menu@rfid:~$')} Entrez l'heure d'entrée (format : dd/mm/YY HH:MM:SS) : \n")
                h_sortie = input(f"{underline('menu@rfid:~$')} Entrez l'heure de sortie (format : dd/mm/YY HH:MM:SS) : \n")
                ajouter_une_entree(badge, porte, h_entree, h_sortie)

        elif menu_selection == 5:
                badge = input(f"{underline('menu@rfid:~$')} Entrez le numéro de série du badge : \n").upper()
                h_entree = input(f"{underline('menu@rfid:~$')} Entrez l'heure d'entrée (format : dd/mm/YY HH:MM:SS) : \n")
                h_sortie = input(f"{underline('menu@rfid:~$')} Entrez l'heure de sortie (format : dd/mm/YY HH:MM:SS) : \n")
                corriger_une_entree(badge, h_entree, h_sortie)

        elif menu_selection == 6:
                montrer_toutes_les_entrees()
        
        elif menu_selection == 7:
                print("Déconnexion...\n")
                break

        else:
                print("Choix invalide\n")

        input("Appuyez sur entrée pour continuer...")

os.system(var)
conn.commit()
conn.close()