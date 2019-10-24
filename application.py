import requests
import sys



def make_url (depart, arrive):
    return "https://www.bonnesroutes.com/distance/?from="+depart+"&to="+arrive
    

def get_html (url):
    reponse = requests.get(url)
    return reponse.text


def html_to_km (html):
    str_part1 = html.split("id=\"total_distance\">")[1] #on découpe le string selon délimiteur "id="total_distance" div class="total_units">
    str_part2 = str_part1.split("<div class=\"total_units\">")[0]
    str_part3 = str_part2.split("\">")[1]
    str_part4 = str_part3.split("</")[0]
    return int(str_part4)

