import requests
import sys
from tabulate import tabulate
# C'est la distance parcourue pendant le temps de démarrage ou de freinage. CONSTANTE
DIST_START =  7.506
# (9-5) * 2 = 8 .4 c'est le temps perdu à freiner sur la distance de freinage * 2 pour l'accelaration | 15 temps de la pause
#differentiel entre temps de pause et temps de route
TPS_PAUSE_M = 8 + 15
TPS_PAUSE_H_DEC = 23 / 60
# temps plein gaz pendant temps DIST_START
# (Hdec_to_H(7.506 / 90))   5min


def make_url (depart, arrive):
    return "https://www.bonnesroutes.com/distance/?from="+depart+"&to="+arrive


def get_html (url):
    reponse = requests.get(url)
    return reponse.text

#  on recupère le kilomètrage entre 2 villes en découpant plusieurs fois le HTML
def html_to_kms (html):
    str_part1 = html.split("id=\"total_distance\">")[1] #on découpe le string selon délimiteur "id="total_distance" div class="total_units">
    str_part2 = str_part1.split("<div class=\"total_units\">")[0]
    str_part3 = str_part2.split("\">")[1]
    str_part4 = str_part3.split("</")[0]
    return int(str_part4)



def get_temps_theorique (kms):
    return kms/90 + 8/60 # 8/60 = temps perdu lors du démrrage et du freinage en minutes


def Hdec_to_H(temps):
    h = int(temps)
    # On retire les heures pour ne garder que les minutes.
    t = (temps - h) * 60 # 0.24 * 60 = temps_restant en minutes.
    m = int(t)
    # On retire les minutes pour ne garder que les secondes.
    t = (t - m) * 60
    s = int(t)
    if s >= 30: 
        m += 1
    return ("{}:{}".format(h, m))


def calcul_nb_pause (temps_theorique):
    return int(temps_theorique / 2)


def get_temps (kms, nb_pause):
    return kms/90 + 8/60 + TPS_PAUSE_H_DEC * nb_pause


def p_print (depart, arrive, kms, temps):
    print(tabulate([[depart, arrive, kms, temps]], headers=['Départ', 'Arrive', 'Kilomètres', 'temps']))


if __name__=="__main__":
    if len(sys.argv) == 3:
        v_depart = sys.argv[1]
        v_arrive = sys.argv[2]
        url = make_url (v_depart, v_arrive)
        html = get_html (url)
        kms = html_to_kms (html)
        temps_theorique = get_temps_theorique(kms)
        nb_pause = calcul_nb_pause(temps_theorique)
        temps_total = get_temps(kms, nb_pause)
        temps = Hdec_to_H(temps_total)
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







