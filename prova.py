# Rete neurale predizione: chi farà prima 10 pt
from pyswip import Prolog
from Partita_class import *
from ProfiloGiocatore_class import *
import pandas as pd
class live:
    def __init__(self,partita, evento, campo_casa, campo_ospite):
        self.giocatori_in_campo_casa = converti_lst(campo_casa)
        self.giocatori_in_campo_ospite = converti_lst(campo_ospite)
        self.evento = evento['evento']
        if self.evento is None:
            self.evento = " "
        self.giocatore = controlla_nome(evento['giocatore']['nome_giocatore'])
        if self.giocatore is None:
            self.giocatore = " "
    def get_evento(self):
        return self.evento
    def get_giocatore(self):
        return self.giocatore
    def get_sq_casa(self):
        return self.giocatori_in_campo_casa
    def get_sq_ospite(self):
        return self.giocatori_in_campo_ospite
    def to_vec(self):
        vet = []
        vet.append(self.get_giocatore())
        vet.append(self.get_evento())
        for giocatore in self.get_sq_casa():
            vet.append(giocatore)
        for giocatore in self.get_sq_ospite():
            vet.append(giocatore)
        return vet
'''
def get_squadra(nome): #dato il nome di una squadra preleva i dati dal csv e ritorna array nomi giocatori
    with open("dataset/squadre.json", "r") as jsonfile:
        squadre = json.load(jsonfile)
    return squadre.get(nome, [])
'''
def quintetto_titolare(partita, nome):
    global player_names
    team1_players = []
    players = set()
    for item in partita["eventi"]:
        player_name = controlla_nome(item["giocatore"]["nome_giocatore"].strip())
        if player_name and player_name not in players:
            players.add(player_name)
            if item["giocatore"]["squadra"] == nome:
                team1_players.append(player_name.split("_"))
            if len(team1_players) == 5:
                return team1_players
            else:
                None
    return team1_players
def same_names(str1, str2):
    return set(str1) == set(str2)
def converti_str(lst):
    return [n.split("_") for n in lst]
def converti_lst(lst):
    return ["_".join(n) for n in lst]

def controlla_nome(nome):
    global player_names
    for na in player_names:
        if nome == na:
            return nome
    name_parts = nome.split("_")
    if len(name_parts) == 2:
        nome2 = name_parts[1]+"_"+name_parts[0]
        for na2 in player_names:
            if nome2 == na2:
                return nome2
    if len(name_parts) == 3:
        nome3 = name_parts[1]+"_"+name_parts[2]+"_"+name_parts[0]
        for na3 in player_names:
            if nome3 == na3:
                return nome3
def fai_cambio(campo_ospite, name, str2):
    for i, giocatore in enumerate(campo_ospite):
        if giocatore == name:
            campo_ospite[i] = str2
    return campo_ospite
def next_10(partita,n_evento):
    for j in range(n_evento, len(partita['eventi'])):
        if(int(partita['eventi'][j]['punti_casa']) >= int(partita['eventi'][n_evento]['punti_casa'])+10):
            return 1
        elif(int(partita['eventi'][j]['punti_ospite'] )>= int(partita['eventi'][n_evento]['punti_ospite'])+10):
            return 0
    if(int(partita['eventi'][len(partita['eventi'])-1]['punti_casa']) > int(partita['eventi'][len(partita['eventi'])-1]['punti_ospite'])):
        return 1
    else:
        return 0

import numpy as np
#Apro tutte le partite e creo il campionato
with open('dataset/partita.json', 'r') as file:
    campionato = json.load(file)

nome = []
squadre = {}
#Per ogni partita creo una lista di eventi live e inserisco questa lista in una lista per tutte le partite
campionato_live = []
Y=[]
giocatori = pd.read_csv('dataset\giocatori.csv')
player_names = giocatori['nome_giocatore'].to_list()
for partita in campionato:
    partita_event_live = []
    if partita['risultato_finale_host'] != '0':
        campo_casa = quintetto_titolare(partita, partita['squadra_casa'])
        campo_ospite = quintetto_titolare(partita, partita['squadra_ospite'])
        pred = []
        i = 0
        for evento in partita['eventi']:
            pred.append(next_10(partita, i))
            if evento['evento'] == "OUT":
                 nome = evento['giocatore']['nome_giocatore'].split("_")
            if evento['evento'] == "IN":
                if evento['giocatore']['squadra'] == partita['squadra_casa']:
                    campo_casa = fai_cambio(campo_casa,nome,evento['giocatore']['nome_giocatore'])
                else:
                    campo_ospite = fai_cambio(campo_ospite,nome,evento['giocatore']['nome_giocatore'])
            partita_event_live.append(live(partita, evento, campo_casa, campo_ospite))
            i = i+1
        campionato_live.append(partita_event_live)
        Y.append(pred)
print("Fine caricamento")

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

from keras.preprocessing.text import Tokenizer
def convert_to_input_format(live_data):
    input_data = []
    for partita in campionato_live:
        for event in partita:
            input_data.append(event.to_vec())
    return input_data

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd

#prendono i nomi dei giocatori piu i ruoli e codificano tutto
giocatori = pd.read_csv('dataset\giocatori.csv')
player_names = giocatori['nome_giocatore'].to_list()
event_names = ['FF', 'FS', 'PP', 'PR', 'RD', 'RO', 'SS', 'SD', 'T2+', 'T3+', 'T1+', 'T2-', 'T3-', 'T1-', 'IN', 'OUT', 'AS', 'SQ', 'EQ', 'TO', 'RT', " "]

# Crea una lista contenente tutti i nomi dei giocatori e gli acronimi degli eventi
names = player_names + event_names
print(names)
# Crea una istanza di LabelEncoder
le = LabelEncoder()
# Adatta l'encoder sulla lista di nomi
le.fit(names)
print(partita_event_live[5].to_vec())
# Converte i nomi in numeri interi
names_encoded = le.transform(partita_event_live[5].to_vec())

print(names_encoded)
# Converti i numeri interi in un array one-hot encoding
inputs = to_categorical(names_encoded)
print(inputs)
targets = Y
# Definire la struttura della rete neurale
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(inputs.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='softmax'))

# Compila il modello
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Allenare la rete neurale
model.fit(inputs, targets, epochs=10, batch_size=32)
