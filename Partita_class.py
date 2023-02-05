import json
class Partita:
    def __init__(self, squadra_casa, squadra_ospite, risultato_finale_host, risultato_finale_guest):
        self.squadra_casa = squadra_casa
        self.squadra_ospite = squadra_ospite
        self.risultato_finale_host = risultato_finale_host
        self.risultato_finale_guest = risultato_finale_guest
        self.eventi = []
    def next_10(self,n_evento):
        for j in range(n_evento, len(self.eventi)):
            if(self.eventi[j].punti_casa >= self.eventi[n_evento].punti_casa+10):
                return 1
            elif(self.eventi[j].punti_ospite >= self.eventi[n_evento].punti_ospite+10):
                return 0
        if(self.eventi[len(self.eventi)-1].punti_casa > self.eventi[len(self.eventi)-1].punti_ospite):
            return 1
        else:
            return 0

class Evento:
    def __init__(self, punti_casa, punti_ospite, evento,quarto, time,giocatore):
        self.punti_casa = punti_casa
        self.punti_ospite = punti_ospite
        self.evento = evento
        self.quarto = quarto
        self.time = time
        self.giocatore = giocatore
class Giocatore:
    def __init__(self, nome_giocatore, numero_giocatore, squadra):
        self.nome_giocatore = nome_giocatore
        self.numero_giocatore = numero_giocatore
        self.squadra = squadra



class PartitaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            return [self.default(partita) for partita in obj]
        elif isinstance(obj, Partita):
            return {'squadra_casa': obj.squadra_casa,
                    'squadra_ospite': obj.squadra_ospite,
                    'risultato_finale_host': obj.risultato_finale_host,
                    'risultato_finale_guest': obj.risultato_finale_guest,
                    'eventi': obj.eventi}
        elif isinstance(obj, Evento):
            return {'punti_casa': obj.punti_casa,
                    'punti_ospite': obj.punti_ospite,
                    'evento': obj.evento,
                    'quarto' : obj.quarto,
                    'time' : obj.time,
                    'giocatore': obj.giocatore}
        elif isinstance(obj, Giocatore):
            return {'nome_giocatore': obj.nome_giocatore,
                    'numero_giocatore': obj.numero_giocatore,
                    'squadra': obj.squadra}
