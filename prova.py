# Rete neurale predizione: chi farà prima 10 pt
from pyswip import Prolog
from Partita_class import *
from ProfiloGiocatore_class import *
class live:
    def __init__(self,partita, evento):
        self.squadra_casa = squadra(partita['squadra_casa'], partita)#5 giocatori in campo
        self.squadra_ospite = squadra(partita['squadra_ospite'], partita)#5 giocatori in campo
        self.evento = evento['evento']
        self.analizza_evento(partita, evento)
    def analizza_evento(self, partita,evento):
        if evento['evento'] == "OUT":
            prolog.assertz("esce_giocatore({}, {})".format(to_lower_and_dashed(evento['giocatore']['nome_giocatore']),to_lower_and_dashed(evento['giocatore']['squadra'])))
class squadra:
    def __init__(self, nome, partita):
        self.nome = to_lower_and_dashed(nome)
        self.squadra_completa = get_squadra(self.nome)
        self.giocatori_in_campo = self.giocatori_in_campo(partita)
    def giocatori_in_campo(self, partita):#Devo inserire i giocatori prima che la partita inizi.
        query = list(prolog.query("giocatori_in_campo({}).".format(to_lower_and_dashed(self.nome))))
        if len(query) == 1:
            quintetto = quintetto_titolare(partita, self.nome)
            for giocatore in quintetto:
                prolog.assertz("entra_giocatore({}, {})".format(to_lower_and_dashed(giocatore),to_lower_and_dashed(self.nome)))
                return quintetto
        else:
            return [x['Giocatore'] for x in query]
    def crea_squadra(self,giocatori, squadra):
        for giocatore in giocatori:
            prolog.assertz("giocatore({}, {})".format(to_lower_and_dashed(giocatore),to_lower_and_dashed(squadra)))

def get_squadra(nome): #dato il nome di una squadra preleva i dati dal csv e ritorna array nomi giocatori
        with open("dataset/squadre.json", "r") as jsonfile:
            squadre = json.load(jsonfile)
            return squadre.get(nome, [])
def to_lower_and_dashed(s):
    return s.lower().replace(" ", "_").replace(".", "_")

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

# SCHIZZO DI RETE

# La rete la addestro su tutte le partite considerando ogni evento uno alla volta come se fosse live
# PROBLEMI
# 1) Sicuramente scalando i dati la miglioro di molto
# 2) Capire come dare importanza alla sequenzialità degli eventi es i 10 eventi prima

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

global prolog
prolog = Prolog()
prolog.consult("prolog/partita.pl")
#Per ogni partita creo una lista di eventi live e inserisco questa lista in una lista per tutte le partite
campionato_live = []
for partita in campionato:
    partita_event_live = []
    if partita['risultato_finale_host'] != '0':
        for evento in partita['eventi']:
            live_event = live(partita, evento)
            partita_event_live.append(live_event)
        print("partita aggiunta")
        campionato_live.append(partita_event_live)

print(campionato_live)

"""
def create_live_dataset(live_data):
    X = []
    Y = []
    for partita in campionato:
        for evento in partita:
            X.append([giocatori(evento.squadra_casa), evento.squadra_ospite), evento.evento, data.ris_casa, data.ris_ospite])
            Y.append(next_10())
        return np.array(X), np.array(Y)


live_data = [live("squadra1", "squadra2", "goal", 1, 0),
             live("squadra2", "squadra3", "fallo", 0, 0),
             live("squadra3", "squadra1", "rigore", 0, 1),
             live("squadra1", "squadra3", "azione", 1, 0),
             live("squadra2", "squadra1", "tiro in porta", 0, 1)]

X, Y = create_live_dataset(live_data)

# Questo modello RNN avrà una struttura a un solo layer LSTM con 10 unità,
# seguita da un layer densamente connesso con una funzione di attivazione sigmoide.
# Il modello viene addestrato su un dataset di 5 esempi con 5 caratteristiche ciascuno,
# utilizzando la funzione di perdita binary_crossentropy e l'ottimizzatore Adam.

# Modello RNN
modello = Sequential()
modello.add(LSTM(10, input_shape=(5, 1)))
modello.add(Dense(1, activation='sigmoid'))
modello.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Addestramento del modello
modello.fit(X.reshape(5, 5, 1), Y, epochs=100, batch_size=1, verbose=1)
"""