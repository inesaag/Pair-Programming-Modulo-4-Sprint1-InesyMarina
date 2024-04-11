#%%
# Funciones necesarias
# ---------------------------------------------
from src import scrapping as scp
from src import data_treatment as dt
import pandas as pd
pd.set_option('display.max_columns', None)

#%%
df_ghibli = dt.open_csv('files/Studio Ghibli.csv')

# -------- Ejecutar el código comentado en caso de necesitar obtener los datos de nuevo (web scrapping)
# df_disney = dt.open_csv('files/DisneyMoviesDataset.csv')
# disney_animation_list = scp.animation_movies_list('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Animation_Studios_films')
# df_disney = dt.get_only_animation(df_disney, disney_animation_list)
# df_disney.to_csv('files/disney_animation.csv')
# df_ghibli_details = scp.movie_data(df_ghibli, 'ghibli')
# df_ghibli_details.to_csv('files/ghibli_details.csv')
# df_disney_details = scp.movie_data(df_disney, 'disney')
# df_disney_details.to_csv('files/disney_details.csv')
# -------------------------------------------------------------------------------

# %%
df_disney = dt.open_csv('files/disney_animation.csv')
df_disney_details = dt.open_csv('files/disney_details.csv')
df_ghibli_details = dt.open_csv('files/ghibli_details.csv')

#%%
df_disney = pd.merge(df_disney, df_disney_details, left_on='title', right_on='title', how='inner')
df_ghibli = pd.merge(df_ghibli, df_ghibli_details, left_on='Name', right_on='title', how='inner')
df_ghibli.drop(['direction', 'title'], axis=1, inplace=True)

# %%
df_disney['direction'] = df_disney['direction'].apply(dt.to_list)
df_disney = dt.separate_directors(df_disney)

# %%
df_disney.head(5)
# %%
df_ghibli.head(5)
# %%
