#%%
# Funciones necesarias
# ---------------------------------------------
from src import scrapping as scp
from src import data_treatment as dt
import pandas as pd
import re
pd.set_option('display.max_columns', None)

# %% -------------------------------------------------------------------- Uncomment & run in case of need to update the scrapping
# df_ghibli = dt.open_csv('files/Studio Ghibli.csv')
# df_disney = dt.open_csv('files/DisneyMoviesDataset.csv')
# disney_animation_list = scp.animation_movies_list('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Animation_Studios_films')
# df_disney = dt.get_only_animation(df_disney, disney_animation_list)
# df_disney.to_csv('files/disney_animation.csv')
# df_ghibli_details = scp.movie_data(df_ghibli, 'ghibli')
# df_ghibli_details.to_csv('files/ghibli_details.csv')
# df_disney_details = scp.movie_data(df_disney, 'disney')
# df_disney_details.to_csv('files/disney_details.csv')

# %% -------------------------------------------------------------------- Uncomment & run in case of need to update the DISNEY files
# df_disney = dt.open_csv('files/disney_animation.csv')
# df_disney_details = dt.open_csv('files/disney_details.csv')
# df_disney = pd.merge(df_disney, df_disney_details, left_on='title', right_on='title', how='inner')
# df_disney['direction'] = df_disney['direction'].apply(dt.to_list)
# df_disney = dt.separate_directors(df_disney)
# df_disney_genre = dt.open_csv('files/disney_movies.csv')
# df_disney_genre = df_disney_genre[['movie_title' , 'genre']]
# df_disney_genre = dt.adding_movies_genre(df_disney_genre)
# df_disney_genre = df_disney_genre.drop_duplicates()
# df_disney = pd.merge(df_disney, df_disney_genre, left_on='title', right_on='movie_title', how='left')
# delete_columns = ['Production company', 'Release date', 'Running time', 'Country', 'Language', 'metascore', 'Directed by', 'Produced by', 'Written by', 'Based on', 'Starring', 'Music by', 'Distributed by', 'Budget', 'Box office', 'Story by', 'Narrated by', 'Cinematography', 'Edited by', 'Screenplay by', 'Production companies', 'Adaptation by', 'Traditional', 'Simplified', 'movie_title']
# df_disney.drop(delete_columns, axis=1, inplace=True)
# df_disney.to_csv('files/disney_clean.csv')

# %% -------------------------------------------------------------------- Uncomment & run in case of need to update the GHIBLI files
# df_ghibli = dt.open_csv('files/Studio Ghibli.csv')
# df_ghibli_details = dt.open_csv('files/ghibli_details.csv')
# df_ghibli = pd.merge(df_ghibli, df_ghibli_details, left_on='Name', right_on='title', how='inner')
# df_ghibli.drop(['title', 'direction', 'Screenplay'], axis=1, inplace=True)
# df_ghibli['Genre 1'] = df_ghibli.apply(lambda x : x['Genre 2'] if x['Genre 1'] == 'Animation' else x['Genre 1'], axis=1)
# df_ghibli.drop(['Genre 2', 'Genre 3'], axis=1, inplace=True)
# df_ghibli.to_csv('files/ghibli_clean.csv')

#%%
df_disney = dt.open_csv('files/disney_clean.csv')
df_ghibli = dt.open_csv('files/ghibli_clean.csv')
# %%
df_disney.drop(['Director 2', 'Director 3'], axis=1, inplace=True) 

df_disney.columns = ['Movie Title', 'Duration', 'Budget', 'Revenue', 'Release Year', 'IMDb', 'Rotten Tomatoes', 'Director', 'Genre']

new_index = ['Movie Title', 'Release Year', 'Director', 'Budget', 'Revenue', 'Genre', 'Duration', 'Rotten Tomatoes', 'IMDb']
df_disney = df_disney.reindex(columns=new_index)

df_disney['Release Year'] = df_disney['Release Year'].apply(lambda x : x.split("-")[0] if isinstance(x, str) else x)

df_disney['Rotten Tomatoes'] = df_disney['Rotten Tomatoes'].apply(lambda x : x.replace("%", "") if isinstance(x, str) else x)

df_disney.loc[df_disney['Movie Title'] == 'Snow White and the Seven Dwarfs', 'Rotten Tomatoes'] = 93
df_disney.loc[df_disney['Movie Title'] == 'Raya and the Last Dragon', 'Rotten Tomatoes'] = 93
df_disney.loc[df_disney['Movie Title'] == 'Raya and the Last Dragon', 'IMDb'] = 7.3
df_disney.loc[df_disney['Movie Title'] == 'Raya and the Last Dragon', 'Duration'] = 107
df_disney.loc[df_disney['Movie Title'] == 'The Little Mermaid', 'Revenue'] = 211343479
df_disney.loc[df_disney['Movie Title'] == 'Raya and the Last Dragon', 'Budget'] = 100000000
df_disney.loc[df_disney['Movie Title'] == 'Raya and the Last Dragon', 'Revenue'] = 130423032
df_disney.loc[df_disney['Movie Title'] == 'Meet the Robinsons', 'Budget'] = 100000000

df_filtrado = df_disney.loc[df_disney['Release Year'].astype(int) < 1990]
media = round(df_filtrado['Budget'].mean(),0)
df_disney['Budget'] = df_disney['Budget'].fillna(media)
df_disney['Budget'] = df_disney['Budget'].astype(float)

df_disney['Revenue'] = df_disney['Revenue'].astype(float)

df_disney['IMDb'] = df_disney['IMDb'].apply(lambda x : int(str(x).replace(".", "")))

df_disney['IMDb'] = df_disney['IMDb'].astype(int)
df_disney['Rotten Tomatoes'] = df_disney['Rotten Tomatoes'].astype(int)
df_disney['Duration'] = df_disney['Duration'].astype(int)

df_disney['Studio'] = 'Disney'
#%%
df_ghibli.columns = ['Movie Title', 'Release Year', 'Director', 'Budget', 'Revenue', 'Genre', 'Duration', 'Rotten Tomatoes', 'IMDb']

patron = r'\(\d{4}\)'
df_ghibli['Movie Title'] = df_ghibli['Movie Title'].apply(lambda x : re.sub(patron, '', x).replace('\n', ''))

df_ghibli['IMDb'] = df_ghibli['IMDb'].apply(lambda x : int(str(x).replace(".", "")))

df_ghibli['Duration'] = df_ghibli['Duration'].apply(lambda x : int(x.split(' ')[0].replace('h', ''))*60 + int(x.split(' ')[1].replace('m', '')))

df_ghibli['Budget'] = df_ghibli['Budget'].str.replace('$', '')
df_ghibli['Budget'] = df_ghibli['Budget'].astype(float)
df_ghibli['Revenue'] = df_ghibli['Revenue'].str.replace('$', '')
df_ghibli['Revenue'] = df_ghibli['Revenue'].astype(float)

df_ghibli['Studio'] = 'Ghibli'

df_ghibli['IMDb'] = df_ghibli['IMDb'].astype(int)
df_ghibli['Rotten Tomatoes'] = df_ghibli['Rotten Tomatoes'].astype(int)


#%%
df_ghibli.head(30)
#%%
df_disney.head(60)
# %%
#df_final = pd.concat([df_disney, df_ghibli]).reset_index()
#df_final.to_csv('files/total_movies.csv')