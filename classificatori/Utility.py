import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import os

def crea_dati():

    giocatori = pd.read_csv(os.path.realpath('giocatori.csv'))

    giocatori = giocatori.drop('nome_giocatore', axis = 1)
    giocatori = giocatori.drop('numero_giocatore', axis = 1)
    giocatori = giocatori.drop('squadra', axis = 1)
    giocatori = giocatori.drop('RIM_D', axis = 1)
    giocatori = giocatori.drop('RIM_O', axis = 1)
    giocatori = giocatori.drop('T1_PER', axis = 1)
    giocatori = giocatori.drop('T2_PER', axis = 1)
    giocatori = giocatori.drop('T3_PER', axis = 1)

    players_without_role = giocatori.loc[(giocatori["ruolo"].isnull()) | (giocatori["ruolo"] == "NaN")]
    players_without_role = players_without_role.drop('ruolo', axis = 1)

    giocatori = giocatori.dropna()

    players_without_role = scale_cols(players_without_role, 'minuti')
    players_without_role = players_without_role.drop('minuti', axis = 1)
    players_without_role["altezza"] = players_without_role["altezza"].replace(0, np.nan, inplace=True)

    giocatori = scale_cols(giocatori, 'minuti')
    giocatori = giocatori.drop('minuti', axis = 1)

    x = giocatori.drop('ruolo', axis=1)
    y = giocatori['ruolo']
    return x, y

# Definire una funzione per scalare i valori di ogni riga
def scale_cols(df, col):
    df = df[df[col] != 0]
    factor = 40/df[col].values
    float_cols = df.select_dtypes(include=['float64']).columns
    float_cols = float_cols.drop(col)
    df.loc[:, float_cols] = df[float_cols].mul(factor, axis=0)
    return df

