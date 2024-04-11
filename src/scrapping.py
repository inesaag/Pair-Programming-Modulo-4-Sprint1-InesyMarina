#%%
# Importar librerías para web scraping y manipulación de datos
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests

# Importar librerías para manipulación y análisis de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np
# Importar librerías para procesamiento de texto
# -----------------------------------------------------------------------
import re

# -----------------------------------------------------------------------
import random
from unidecode import unidecode 

# -----------------------------------------------------------------------
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# -----------------------------------------------------------------------
from time import sleep  

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


def movie_data (df, type):
    
    # Inicia el navegador Chrome en español
    options = webdriver.ChromeOptions()
    options.add_argument("--accept-lang=es")
    driver = webdriver.Chrome(options=options)
    datos = []
    
    if type == "ghibli":
        
        # Abre la página de IMDb
        driver.get("https://www.google.es/")
        driver.maximize_window()
    
        # Rechaza las cookies en caso de haberlas
        try:
            driver.find_element("css selector" , "#W0wltc").click()
            
        except:
            pass
        
        sleep(random.uniform(1.5 , 2.0))
    
        for i in range(0, len(df)):
            
            nombre_peli = df['Name'][i]
            anio_peli = df['Year'][i]
            string_buscar = f"{nombre_peli} ({anio_peli}) rotten tomatoes score"
            
            espera = 60
            buscador = WebDriverWait(driver , espera).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#APjFqb")))
            buscador.send_keys(string_buscar, Keys.ENTER)
            sleep(random.uniform(1.5 , 2.0))
            
            for resultado in range (1 , 5): 
                
                try:
                
                    # Obtiene los datos del resultado de búsqueda según rango
                    datos_resultado = driver.find_element('css selector', f'#rso > div:nth-child({resultado}) > div > div').text.split("\n")   
                    # Condición para verificar si en el segundo elemento de los resultados de búsqueda aparece 'rotten tomatoes' (así sabemos que la información está sacada de su página)
                    if datos_resultado[1].lower() == 'rotten tomatoes':
                        
                        if 'Valoración:' in datos_resultado[-1]:
                            valoracion = datos_resultado[-1]
                            puntuacion_rotten = re.search('(\d+)%' , valoracion).group(1)
                            puntuacion_rotten = float(puntuacion_rotten.replace("%" , "")) # Si encuentra la valoración, asigna su valor a la variable
                            break 
                        
                        elif 'Valoración' in datos_resultado[-2]:
                            valoracion = datos_resultado[-2]
                            puntuacion_rotten = re.search('(\d+)%' , valoracion).group(1)
                            puntuacion_rotten = float(puntuacion_rotten.replace("%" , "")) # Si encuentra la valoración, asigna su valor a la variable
                            break 
                            
                        else:
                            puntuacion_rotten = np.nan # Si no encuentra la valoración, le asigna '-' por defecto

                        break
                except:
                    pass
            
            limpieza = WebDriverWait(driver, espera).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tsf > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.BKRPef > div")))
            limpieza.click()
            
            string_buscar = f"{nombre_peli} ({anio_peli}) imdb score"
            
            espera = 60
            buscador = WebDriverWait(driver , espera).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#APjFqb")))
            buscador.send_keys(string_buscar, Keys.ENTER)
            sleep(random.uniform(1.5 , 2.0))
            
            for resultado in range (1 , 5): 
                
                try:
                
                    # Obtiene los datos del resultado de búsqueda según rango
                    datos_resultado = driver.find_element('css selector', f'#rso > div:nth-child({resultado}) > div > div').text.split("\n")   
                    # Condición para verificar si en el segundo elemento de los resultados de búsqueda aparece 'rotten tomatoes' (así sabemos que la información está sacada de su página)
                    if datos_resultado[1].lower() == 'imdb':
                        
                        if 'Valoración:' in datos_resultado[-1]:
                            valoracion = datos_resultado[-1]
                            puntuacion_imdb = re.search(r'(\d(?:,\d)?)\/10', valoracion).group(1)
                            puntuacion_imdb = float(puntuacion_imdb.replace("," , ".")) # Si encuentra la valoración, asigna su valor a la variable
                            break 
                        
                        elif 'Valoración' in datos_resultado[-2]:
                            valoracion = datos_resultado[-2]
                            puntuacion_imdb = re.search(r'(\d(?:,\d)?)\/10', valoracion).group(1)
                            puntuacion_imdb = float(puntuacion_imdb.replace("," , ".")) # Si encuentra la valoración, asigna su valor a la variable
                            break 
                            
                        else:
                            puntuacion_imdb = np.nan # Si no encuentra la valoración, le asigna '-' por defecto
                            break
                except:
                    pass
            
            limpieza = WebDriverWait(driver, espera).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tsf > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.BKRPef > div")))
            limpieza.click()
            sleep(random.uniform(1.5 , 2.0))
        
        column_names = ['title', 'rotten_score', 'imdb_score']
        
        df = pd.DataFrame(datos, columns=column_names)
    
    elif type == 'disney':
        
        driver.get("https://www.imdb.com/")
        driver.maximize_window()
        
        sleep(random.uniform(1.5 , 2.0))
        
        # Acepta las cookies si es necesario
        try:
            driver.find_element("css selector" , "#__next > div > div > div.sc-jrcTuL.bPmWiM > div > button.icb-btn.sc-bcXHqe.sc-hLBbgP.sc-ftTHYK.dcvrLS.dufgkr.ecppKW").click()
        except:
            pass
        
        for i in range(0, len(df)):
            
            nombre_peli = df['title'][i]
            anio_peli = df['Release date (datetime)'][i]
            anio_peli = anio_peli.split("-")[0]
            string_buscar = f"{nombre_peli} ({anio_peli})"
            
            espera = 60
            buscador = WebDriverWait(driver , espera).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#suggestion-search")))
            buscador.send_keys(string_buscar)

            resultado = WebDriverWait(driver, espera).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-autowhatever-navSuggestionSearch--item-0 > a")))
            resultado.click()
            
            sleep(random.uniform(1.5 , 2.0))
            
            info = driver.find_element('xpath' , f'//*[@id="__next"]/main/div/section[1]/section/div[3]/section').text 
            info = info.split('\n')
            
            for indice, dato in enumerate(info):
                
                separador = re.compile(r'(?<=[a-z])(?=[A-Z])')
                
                if 'direccion' == unidecode(dato.lower()):
                    
                    datos_direccion = info[indice+1]
            
                    # Utiliza el patrón de regex para separar los elementos de la string
                    datos_direccion = separador.split(datos_direccion)
                    
                    if len(datos_direccion) == 1:
                        datos_direccion = datos_direccion[0]
            
            
            tupla = (nombre_peli , datos_direccion) # Genera una tupla 
            datos.append(tupla) # Añade la tupla a la lista
            
            sleep(random.uniform(1.0, 1.5))
            
        column_names = ['title', 'direction']
        
        df = pd.DataFrame(datos, columns=column_names)
        
    return df