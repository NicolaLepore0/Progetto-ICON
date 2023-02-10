
import numpy as np
from sklearn.mixture import GaussianMixture
import pandas as pd
from sklearn.cluster import KMeans
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.utils.extmath import row_norms
from sklearn.datasets._samples_generator import make_blobs
from timeit import default_timer as timer

os.environ['OMP_NUM_THREADS'] = '1'

# Carica il dataset in un dataframe di pandas
giocatori = pd.read_csv("dataset/giocatori.csv")
giocatori = giocatori.drop('nome_giocatore', axis=1)
giocatori = giocatori.drop('numero_giocatore', axis=1)
giocatori = giocatori.drop('squadra', axis=1)
giocatori = giocatori.dropna()
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


# Seleziona le colonne che vuoi utilizzare come feature
features = ['ruolo','altezza', 'T2_T', 'T2_PER', 'T3_T', 'T3_PER', 'RIM_O', 'RIM_D', 'RIM_T', 'STOP_D', 'STOP_S', 'ASS']

X = giocatori[features].values

X = X[:, ::-1]



import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.utils.extmath import row_norms
from sklearn.datasets._samples_generator import make_blobs
from timeit import default_timer as timer

print(__doc__)

# Generate some data
def get_initial_means(X, init_params, r):
    # Run a GaussianMixture with max_iter=0 to output the initalization means
    gm = GaussianMixture(n_components=4,covariance_type='full', tol=0.001, reg_covar=1e-06, max_iter=100, n_init=1,
                         init_params='k-means++', weights_init=None, means_init=None, precisions_init=None, random_state=None,
                         warm_start=False, verbose=0, verbose_interval=10).fit(X)
    return gm.means_


methods = ["kmeans", "random_from_data", "k-means++", "random"]
colors = ["navy", "turquoise", "cornflowerblue", "darkorange"]
times_init = {}
relative_times = {}

plt.figure(figsize=(4 * len(methods) // 2, 6))
plt.subplots_adjust(
    bottom=0.1, top=0.9, hspace=0.15, wspace=0.05, left=0.05, right=0.95
)

for n, method in enumerate(methods):
    r = np.random.RandomState(seed=1234)
    plt.subplot(2, len(methods) // 2, n + 1)

    start = timer()
    ini = get_initial_means(X, method, r)
    end = timer()
    init_time = end - start

    gmm = GaussianMixture(
        n_components=4, means_init=ini, tol=1e-9, max_iter=2000, random_state=r
    ).fit(X)

    times_init[method] = init_time
    for i, color in enumerate(colors):
        data = X[gmm.predict(X) == i]
        plt.scatter(data[:, 0], data[:, 1], color=color, marker="x")

    plt.scatter(
        ini[:, 0], ini[:, 1], s=75, marker="D", c="orange", lw=1.5, edgecolors="black"
    )
    relative_times[method] = times_init[method] / times_init[methods[0]]

    plt.xticks(())
    plt.yticks(())
    plt.title(method, loc="left", fontsize=12)
    plt.title(
        "Iter %i | Init Time %.2fx" % (gmm.n_iter_, relative_times[method]),
        loc="right",
        fontsize=10,
        )
plt.suptitle("GMM iterations and relative time taken to initialize")
plt.show()
