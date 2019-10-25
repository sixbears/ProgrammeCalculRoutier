import requests
import sys
from tabulate import tabulate


# Distance parcourue à 10kms/h en 1 min = 10/60 = 0.1666..

# Distance parcourue pendant le temps de démarrage soit 9min
# DIST_START = 0
# for i in range(1:8):
#     DIST_START += i * 10/60 

# Distance parcourue de 0 à 80kms/h en 8 min (résultat de la boucle)
# DIST_START = 14/3 = 4.6666..


# Temps pour parcourir 4.6666kms à 90km/h en minutes décimales
# TPS_SPEED = 14/3 / 90 * 60 = 3.1111

# Différence de temps entre démarrage et à 90km/h sur 4.666km
# DIFF1 = 8 - 3.1111 = 4.8889 -- 4min53

# DITS_START = DIST_STOP ==> on multiplie par 2 ce temps
# DIFF2 = 9.7778 -- 9min46

# On ajoute le temps de pause de 15 min
# DIFF_TOTALE = 9.7778 + 15 = 24.7778

# Différentiel entre temps de pause et temps de route en heure décimales
TPS_PAUSE_H_DEC = 24.7778 / 60 # -- 0.4129633... 24min46


# ######
# # Distance parcourue à 90kms/h en 8 min
# # DIST_SPEED = 12
# # DIST_SPEED - DIST_START = 22/3 = 7.3333..
# ###########
# # 8 - TPS_SPEED = 

# # DITS_START = DIST_STOP ==> on multiplie par 2 la différence de 


# # (9-5) * 2 = 8 
# #  . 4 c'est le temps perdu à freiner sur la distance de freinage * 2 pour l'accelaration | 15 temps de la pause
# # Differentiel entre temps de pause et temps de route
# TPS_PAUSE_H_DEC = 23 / 60
# # temps plein gaz pendant temps DIST_START
# # (Hdec_to_H(7.506 / 90))   5min

# On effectue une recherche internet avec les villes en paramètres
def make_url (depart, arrivee):
    return "https://www.bonnesroutes.com/distance/?from="+depart+"&to="+arrivee

# On récupère le contenu de la recherche internet
def get_html (url):
    reponse = requests.get(url)
    return reponse.text


# On recupère le kilomètrage entre 2 villes en découpant plusieurs fois le HTML
def html_to_kms (html):                                             #On coupe:
    str_part1 = html.split("id=\"total_distance\">")[1]             #En haut!
    str_part2 = str_part1.split("<div class=\"total_units\">")[0]   #En bas!
    str_part3 = str_part2.split("\">")[1]                           #A gauche!    
    str_part4 = str_part3.split("</")[0]                            #A droite!
    return int(str_part4)                                           #Le chiffre est là!


# On retourne le temps de trajet sans les pauses
def get_temps_theorique (kms):
    return kms/90 + 8/60 # 8/60 = temps perdu lors du démarrage et du freinage en minutes

# On transforme uen date au format 2,5h à 2h30
def Hdec_to_H(temps):
    t = temps
    h = int(t)
    # On retire les heures pour ne garder que les minutes.
    t = (t - h) * 60 # 0.24 * 60 = temps_restant en minutes.
    m = int(t)
    # On retire les minutes pour ne garder que les secondes.
    t = (t - m) * 60
    s = int(t)
    if s >= 30: 
        m += 1
    return ("{}:{}".format(h, m))


# On récupère le nombre de pause pour un trajet
def calcul_nb_pause (temps_theorique):
    return int(temps_theorique / 2)


# On recupère le temps réel du trajet en comptant les pauses
def get_temps (kms, nb_pause):
    return kms/90 + 8/60 + TPS_PAUSE_H_DEC * nb_pause # 8/60 = temps perdu lors du démarrage et du freinage en minutes


# On retourne un joli tableau 
def p_print (depart, arrivee, kms, temps):
    print(tabulate([[depart, arrivee, kms, temps]], headers=['Départ', 'Arrivée', 'Kilomètres', 'temps']))


if __name__ == "__main__":
    # On vérifie le nombre d'argument
    if len(sys.argv) == 3:
        # On stocke la ville de départ
        v_depart = sys.argv[1]
        # On stocke la ville d'arrivée
        v_arrive = sys.argv[2]
        # On fait la recherche web concernant la ville d'arrivée et de départ
        url = make_url (v_depart, v_arrive)
        # On stocke le contenu de la recherche 
        html = get_html (url)
        # On stocke le kilomètrage
        kms = html_to_kms (html)
        # On calcul le temps du trajet sans les pauses
        temps_theorique = get_temps_theorique(kms)
        # On calcul le nombre de pause 
        nb_pause = calcul_nb_pause(temps_theorique)
        # On calcul de temps de trajet réel 
        temps_total = get_temps(kms, nb_pause)
        # On convertie le temps au format HH:MM
        temps = Hdec_to_H(temps_total)
        # On retourne le résultat dans le terminal
        p_print(v_depart, v_arrive, kms, temps)
    else :
        print("Nombre d'argument incorrecte")





#     '''
#     get args, si moins long que 2 ou plus -> erreur (if len(args<3) ou len(args>3): else msg d'erreur)
#     make url
#     get html
#     html to km
#     ALGO
#     pprint

#     '''







