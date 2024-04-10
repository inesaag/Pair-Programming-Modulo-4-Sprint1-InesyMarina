# Tratamiento de datos
import pandas as pd
import numpy as np
import re

# Imputación de nulos usando métodos avanzados estadísticos
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# Evaluar linealidad de las relaciones entre las variables
import scipy.stats as stats
from scipy.stats import kstest
from scipy.stats import levene
from scipy.stats import f_oneway
from scipy.stats import kruskal


def open_csv (route):
    
    # Carga el df
    df = pd.read_csv(route)

    # Si al cargar el dataframe se creó una columna de unnamed, la elimina
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis = 1, inplace=True)
        
    return df


def get_only_animation (df , list):
    
    # Crea una columna booleana que pone 'True' si encuentra el nombre en la lista de títulos animados de Wikipedia
    df['Animation'] = df['title'].apply(lambda x : True if x in list else False)
    
    # Crea un nuevo df sólo con aquellas películas animadas
    df = df[df['Animation']]
    
    # Elimina los duplicados (como Disney hizo live action de sus películas animadas, para que no los tenga en cuenta)
    df.drop_duplicates(subset='title', keep='first', inplace=True)
    
    # Restablece los índices
    df = df.reset_index()
    
    # Elimina las columnas sobrantes
    df.drop(['Animation', 'index'], axis = 1, inplace = True)
    
    return df

