import requests
import re
from bs4 import BeautifulSoup
from pyshorteners import Shortener


def clean_name(text:str):
    return text.replace('<td>', '').replace('</td>', '')



def clean_url(text:str):
    return text.split('<a href="')[-1].split('"')[0]



def get_url(url:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    
    refused = [
        'Idioma', 
        'Permisos', 
        'Arquitectura', 
        'Clasificación de contenido', 
        'Publicidad', 
        '¿Por qué se ha publicado esta aplicación en Uptodown?', 
        'Requisitos'
    ]
    
    patron = r"\.[^.]+\.uptodown\.com"
    if re.search(patron, url):
        patron = r"\.[^.]+(?=\.uptodown\.com)"
        url = re.sub(patron, "", url)
    
    if 'descargar' != url.split('/')[-1]:
        url = url + '/descargar'
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_url = soup.find(id='detail-download-button').get('data-url')
    info = soup.find(id='technical-information')
    tabla = info.find('table', class_='content')
    
    icon = soup.find('div', class_='icon').find('img').get('src')

    name = info.find('div', class_='title-row').find('h2').text
    name = name.split('Información sobre ')[-1].lower().replace(' ', '-').replace('.', '-')
    
    json = {}
    for i in tabla.find_all('tr'):
        key = str(i.find_all('td')[-2]).split('<td scope="row">')[-1].split('\n')[0].replace('<td>', '').replace('</td>', '')
        key = clean_name(key)
        value = clean_name(str(i.find_all('td')[-1]))
        if key == 'Categoría':
            value = clean_url(value)
        elif key == 'Autor':
            value = clean_url(value)
            
        if key not in refused:
            json[key] = value
    
    enlace = 'https://dw.uptodown.net/dwn/' + data_url + name + f'.{json["Tipo de archivo"].lower()}'
    s = Shortener()
    enlace_corto = s.isgd.short(enlace)
    json['Enlace'] = enlace
    json['Enlace corto'] = enlace_corto
    json['Icono'] = icon
    
    return json


