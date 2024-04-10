#%%
# Importar librerías para web scraping y manipulación de datos
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests

# Importar librerías para manipulación y análisis de datos
# -----------------------------------------------------------------------
import pandas as pd

# Importar librerías para procesamiento de texto
# -----------------------------------------------------------------------
import re

#%%

def animation_movies_list (url):
    
    # Obtiene la respuesta de la url
    res_url = requests.get(url)
    
    # Parsea el contenido HTML de la respuesta usando BeautifulSoup
    soup_url = BeautifulSoup(res_url.content, 'html.parser')
    
    # Encuentra todas las tablas en la página
    all_tables = soup_url.find_all("table")
    
    # Asigna la sexta tabla (la que contiene la info de las películas) a la variable 'table'
    table = all_tables[5]
    
    # Encuentra todas las filas en la tabla
    rows = table.find_all("tr")
    
    animation_movies = []
    
     # Itera sobre las filas, comenzando desde la tercera fila (índice 2) para evitar encabezados
    for row in rows[2:]:
        
        # Divide el texto de la fila en elementos separados por saltos de línea
        row_elements = row.text.split("\n")
        
        # El segundo elemento en la lista split es el nombre 
        name = row_elements[1]
        
        # Verifica si el nombre encontrado no contiene la frase "as Walt Disney"
        if 'as Walt Disney' not in name:
            # Si no contiene la frase, añade el nombre a la lista de películas de animación
            animation_movies.append(name)
        else:
            # Si contiene la frase, lo omite y pasa a la siguiente
            pass
        
    return animation_movies