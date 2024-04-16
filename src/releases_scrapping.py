import pandas as pd
from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from time import sleep  
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime

#función para sacar las fechas de estreno de imdb
def release_dates(lista):
    releases=[]
    driver = webdriver.Chrome() 

    url = "https://www.google.com/" 

    driver.get(url)  

    driver.maximize_window()

    sleep(1)

    driver.find_element("css selector", "#L2AGLb > div").click() 

    sleep(1)


    for movie in lista:

        driver.find_element("css selector", "#APjFqb").send_keys(f"{movie} release info imdb", Keys.ENTER)  #búsqueda en google

        sleep(4)
        print("----------")
        print(movie)
        
        #click en el primer resultado
        driver.find_element("css selector", "#rso > div:nth-child(1) > div").click()
        #acceptar cookies
        driver.find_element("css selector", "#__next > div > div > div.sc-jrcTuL.bPmWiM > div > button.icb-btn.sc-bcXHqe.sc-dkrFOg.sc-iBYQkv.dcvrLS.ddtuHe.dRCGjd").click() 
        
        sleep(10)
        #ver más
        espera = 10
        elemento = WebDriverWait(driver, espera).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[2]/ul/div/span[2]/button')))           
        elemento.click()
      
        for num in range(1, 21): #cojo elementos, cuando pueda hacer click en el 50 más habrá que subir los números
            country = driver.find_element("css selector", f"#rel_{num} > a.ipc-metadata-list-item__label.ipc-metadata-list-item__label--link").text
            date = elemento = driver.find_element("css selector", f"#rel_{num} > div").text   
                                
            if '(' in date:
                date = re.split(r'(?<=\d{4})', date, maxsplit=1)
                #date.split('(')
                print(f"{num}: {movie}, {country}, {date[0]}")
                releases.append({"movie" : movie, "country" :country, "date" : date[0], "filtro" : date[1]})
            else:
                print(f"{num}: {movie}, {country}, {date}")
                releases.append({"movie" : movie, "country" :country, "date" : date})
        driver.back()
        limpieza = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tsf > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.BKRPef > div")))
        limpieza.click()
    driver.quit()  # Cerrar el navegador al finalizar
    return releases

#modificar la columna date para poder unificarla 
def replace_month(date):
    meses = {
    'enero': 'january',
    'febrero': 'February',
    'marzo': 'March',
    'abril': 'April',
    'mayo': 'May',
    'junio': 'June',
    'julio': 'July',
    'agosto': 'August',
    'septiembre': 'September',
    'octubre': 'October',
    'noviembre': 'November',
    'diciembre': 'December'}
    date = date.replace(' de ', ' ')
    for mes_es, mes_en in meses.items():
        date = date.replace(mes_es, mes_en)
    return date

#pasarla a datetime:
def convert_datetime(date_string):
    try:
        return pd.to_datetime(date_string, format='%d %B %Y')
    except ValueError:
        try:
            return pd.to_datetime(date_string, format='%B %Y')
        except ValueError:
            try:
                return pd.to_datetime(date_string, format='%Y')
            except ValueError:
                return pd.to_datetime(date_string, format='%B %d, %Y')