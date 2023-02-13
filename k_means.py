import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import os

os.environ['OMP_NUM_THREADS'] = '1'

# Carica il dataset in un dataframe di pandas
giocatori = pd.read_csv("dataset/giocatori.csv")
giocatori = giocatori.drop('nome_giocatore', axis=1)
giocatori = giocatori.drop('numero_giocatore', axis=1)
giocatori = giocatori.drop('squadra', axis=1)

def replace_role(row):
    if row['ruolo'] == 'Centro':
        return 0
    elif row['ruolo'] == 'Ala':
        return 1
    elif row['ruolo'] == 'Guardia':
        return 2
    elif row['ruolo'] == 'Play':
        return 3
    else:
        return 3


giocatori['ruolo'] = giocatori.apply(replace_role, axis=1)


# Definire una funzione per scalare i valori di ogni riga
def scale_cols(df, col):
    df = df[df[col] != 0]
    factor = 40 / df[col].values
    float_cols = df.select_dtypes(include=['float64']).columns
    float_cols = float_cols.drop(col)
    df.loc[:, float_cols] = df[float_cols].mul(factor, axis=0)
    return df


giocatori = scale_cols(giocatori, 'minuti')

# Seleziona le colonne che vuoi utilizzare come feature
features = ['ruolo','altezza', 't2_t', 't2_per', 't3_t', 't3_per', 'rim_o', 'rim_d', 'rim_t', 'stop_d', 'stop_s', 'ass']

X = giocatori[features].values

# Inizializza il modello K-means con un numero di cluster definito (ad esempio, 5 cluster)
kmeans = KMeans(n_clusters=4, n_init=10)

# Fit il modello sui dati
kmeans.fit(X)

# Prevedi i cluster a cui appartengono ogni giocatore
labels = kmeans.predict(X)

for i in range(4):
    x = X[labels == i, 0]
    y = X[labels == i, 1]
    plt.scatter(x, y, label='Cluster {}'.format(i+1))

# Aggiungi le etichette per l'asse X e Y
plt.xlabel('Ruolo')
plt.ylabel('altezza')

# Mostra la legenda
plt.legend()

# Mostra il grafico
plt.show()

from sklearn.metrics import silhouette_score

silhouette_score = silhouette_score(X, labels)
print("Silhouette Score: ", silhouette_score)
