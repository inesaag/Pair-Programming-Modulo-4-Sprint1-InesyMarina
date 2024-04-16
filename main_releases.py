import pandas as pd
import re
from src import releases_scrapping as sp


disney = pd.read_csv('files/disney_animation.csv', index_col= 0)
ghibli = pd.read_csv('files/Studio Ghibli.csv', index_col= 0)
ghibli.reset_index(inplace=True)

disney = pd.read_csv('files/disney_clean.csv', index_col= 0)
disney_movies = disney['title'].to_list()

#saco los nombres de las películas de los dataframes
disney_movies = disney['title'].to_list()
ghibli_movies = ghibli['Name'].tolist()

#limpio los nombres de las de ghibli (vienen con el año)
ghibli_movies_clean = []
for movie in ghibli_movies:
    try:
        movie_clean = movie.split('\n')[0]
        ghibli_movies_clean.append(movie_clean)

    except:
        ghibli_movies_clean.append(movie)
ghibli_movies = ghibli_movies_clean

#llamo a la funcion de scrapeo
ghibli_releases = sp.release_dates(ghibli_movies)
disney_releases = sp.release_dates(disney_movies)

#limpio los 'filtros' en disney
palabras = ['DVD', 're-release', 'Blu-ray']

for release in disney_releases:
    if len(release) > 3:
        for palabra in palabras:
            if palabra in release['filtro']:
                disney_releases.remove(release)

#limpio los 'filtros' en ghibli
for release in ghibli_releases:
    if len(release) > 3:
        for palabra in palabras:
            if palabra in release['filtro']:
                ghibli_releases.remove(release)

#despues de la limpieza quitamos todos los 'filtro' que han quedado
for release in disney_releases:
    if len(release) > 3:
        release.popitem()  

for release in ghibli_releases:
    if len(release) > 3:
        release.popitem()  

#convierto en dataframe
df_disney = pd.DataFrame(disney_releases)
df_ghibli = pd.DataFrame(ghibli_releases)

#añado el estudio al que pertenecen antes de unificar tablas
df_disney['studio'] = 'disney'
df_ghibli['studio'] = 'ghibli'
#unifico ambas tablas
releases = pd.concat([df_disney, df_ghibli], axis=0)

#aplico la funcion para limpiar fecha
releases['date'] = releases['date'].apply(lambda x: sp.replace_month(x))

#aplico la funcion para pasar a datetime
releases['date'] = releases['date'].apply(sp.convert_datetime)

#guardar resultado
releases.to_csv('files/total_releases.csv')