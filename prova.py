# Rete neurale predizione: chi farà prima 10 pt
from pyswip import Prolog
from Partita_class import *
from ProfiloGiocatore_class import *
class live:
    def __init__(self,partita, evento, campo_casa, campo_ospite):
        self.giocatori_in_campo_casa = campo_casa
        self.giocatori_in_campo_ospite = campo_ospite
        self.squadra_casa = get_squadra(partita['squadra_casa'])
        self.squadra_ospite = get_squadra(partita['squadra_ospite'])
        self.evento = evento['evento']
def get_squadra(nome): #dato il nome di una squadra preleva i dati dal csv e ritorna array nomi giocatori
    with open("dataset/squadre.json", "r") as jsonfile:
        squadre = json.load(jsonfile)
    return squadre.get(nome, [])
def quintetto_titolare(partita , nome):
    team1_players = []
    players = set()
    for item in partita["eventi"]:
        player_name = item["giocatore"]["nome_giocatore"].strip()
        if player_name and player_name not in players:
            players.add(player_name)
            if item["giocatore"]["squadra"] == nome:
                team1_players.append(player_name)
            if len(team1_players) == 5:
                return team1_players
            else:
                None
    return team1_players
def replace_element(lista, elemento, nuovo_elemento):
    # Trova la posizione dell'elemento da sostituire
    posizione = lista.index(elemento)
    # Sostituisce l'elemento
    lista[posizione] = nuovo_elemento
    return lista
# SCHIZZO DI RETE

# La rete la addestro su tutte le partite considerando ogni evento uno alla volta come se fosse live
# PROBLEMI
# 1) Sicuramente scalando i dati la miglioro di molto

# COSE DA FARE
# 1)applicare la funzione prossimi 10 pt quando sposto i dati per addestramento
# ------for per ogni evento in cui calcolo il live e addestra la rete sapendo che tutto è etichettato
# 1) frame per esportare i dati dalla partita uno alla volta
# 2) come formattarare i dati per passarli mediante database.
# 3) capire come addestrare la rete in maniera sequenziale   FATTO bisogna usare LSTM
# ------per fare questo penso che debba usare model.save('model.h5')
# -------     from keras.models import load_model       model = load_model('model.h5')

import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
#Apro tutte le partite e creo il campionato
with open('dataset/partita.json', 'r') as file:
    campionato = json.load(file)

nome = []
squadre = {}
#Per ogni partita creo una lista di eventi live e inserisco questa lista in una lista per tutte le partite
campionato_live = []
for partita in campionato:
    partita_event_live = []
    if partita['risultato_finale_host'] != '0':
        campo_casa = quintetto_titolare(partita, partita['squadra_casa'])
        campo_ospite = quintetto_titolare(partita, partita['squadra_ospite'])
        for evento in partita['eventi']:
            if evento['evento'] == "OUT":
                 nome = str(evento['giocatore']['nome_giocatore'])
            if evento['evento'] == "IN":
                if evento['giocatore']['squadra'] == partita['squadra_casa']:
                    campo_casa = replace_element(campo_casa,nome,evento['giocatore']['nome_giocatore'])
                else:
                    campo_ospite = replace_element(campo_ospite,nome,evento['giocatore']['nome_giocatore'])
            partita_event_live.append(live(partita, evento, campo_casa, campo_ospite))
        print("partita aggiunta")
        campionato_live.append(partita_event_live)

print('campionato_live')
print(campionato_live)
