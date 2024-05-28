import requests
import json
from string import Template

# Plantilla HTML para la página de aves
html_template = Template('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aves de Chile</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: black;
            color: white;
            line-height: 0.2;             
        }
        h1 {
            font-size: 60px;
            background-color: grey;
            padding: 60px;                          
        }
        h2 {
            font-size: 30px
        }                 
        img {
            border-radius: 5%;
            margin-bottom: 50px;             
        }                  
    </style>
</head>
<body>
    <h1>Aves de Chile</h1>
    $body
</body>
</html>
''')

# Plantilla para cada elemento de ave
elem_template = Template('''
<h2>Nombre: $nombre_ave_espanol</h2>
<h2>Name: $nombre_ave_ingles</h2>
<img src="$url" width="800px">
''')
# Función para realizar una solicitud GET a la URL proporcionada y devolver la respuesta en formato JSON.
# url: La URL a la que se realiza la solicitud GET.
def requests_get(url):
    response = requests.get(url)
    response.raise_for_status()  # Verifica si hubo algún error en la solicitud
    return response.json()
# Función para construir el HTML de la página utilizando los datos obtenidos de la API de aves.
# url: La URL de la API de aves desde donde se obtienen los datos.
def build_html(url):
    # Obtiene la respuesta de la API de aves.
    response = requests_get(url)
    texto = ' '
    # Itera sobre cada ave en la respuesta y utiliza la plantilla para agregar su información al HTML.
    for aves in response:
        nombre = aves['name']['spanish']
        nombre_ingles = aves['name']['english']
        imagen_url = aves['images']['full']
        # Sustituye los valores en la plantilla y agrega el resultado al texto.
        texto += elem_template.substitute(nombre_ave_espanol = nombre, nombre_ave_ingles = nombre_ingles, url = imagen_url)
        # Sustituye el cuerpo del HTML con el texto completo de todas las aves.
    return html_template.substitute(body = texto)

# Generar el HTML y guardarlo en un archivo llamado "index.html"
html = build_html('https://aves.ninjas.cl/api/birds')

with open("index.html", "w", encoding = 'utf-8') as f:
    f.write(html)