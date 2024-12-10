import utils
from utils import get_closest_post
import pandas as pd

path = '/Users/matthiasmolenat/repos/congestion/data/capareseau_ram.csv'

df = pd.read_csv(path)

my_GeopointPoste_1 = [48.5587213, 7.7976421]
my_GeopointPoste_2 = [49.3132494, 1.1897809]
my_GeopointPoste_3 = [49.263092, 4.100068] # Cernay
my_GeopointPoste_4 = [46.754655, 5.915800] # Champagnolle
my_GeopointPoste_5 = [48.7098768941521, 1.3839132342552853] # Les Arpents
n_voisins = 20

df_res = get_closest_post(df,my_GeopointPoste_5, n_voisins)

df_res = df_res[["Code","Nom", "dist_to_my_poste_km","RAM_injection", "RAM_sous_tirage", "Capacité de transformation HTB/HTA restante disponible pour l'injection sur le réseau public de distribution"]]

df_res