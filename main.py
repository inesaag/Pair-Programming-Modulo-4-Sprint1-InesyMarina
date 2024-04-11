#%%
# Funciones necesarias
# ----------------------------------------------
from src import scrapping as scp
from src import data_treatment as dt

#%%
disney_animation_list = scp.animation_movies_list('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Animation_Studios_films')

#%%
df_disney = dt.open_csv('files/DisneyMoviesDataset.csv')
df_ghibli = dt.open_csv('files/Studio Ghibli.csv')

#%%
df_disney = dt.get_only_animation(df_disney, disney_animation_list)
df_disney.to_csv('files/disney_animation.csv')

#%%
df_ghibli_details = scp.movie_data(df_ghibli, 'ghibli')

#%%
df_ghibli_details.to_csv('files/ghibli_details.csv')

# %%
df_disney_details = scp.movie_data(df_disney, 'disney')

# %%
df_disney_details.to_csv('files/disney_details.csv')
# %%
