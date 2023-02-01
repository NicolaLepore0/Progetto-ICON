import json
class ProfiloGiocatore:
    def __init__(self, nome_giocatore, numero_giocatore, squadra, ruolo, altezza):
        self.nome_giocatore = nome_giocatore
        self.numero_giocatore = numero_giocatore
        self.squadra = squadra
        self.ruolo = ruolo
        self.altezza = altezza
        self.minuti = None
        self.FALLI_C = None
        self.FALLI_S = None
        self.T2_R = None
        self.T2_T = None
        self.T2_PER = None
        self.T3_R = None
        self.T3_T = None
        self.T3_PER = None
        self.T1_R = None
        self.T1_T = None
        self.T1_PER = None
        self.RIM_O = None
        self.RIM_D = None
        self.RIM_T = None
        self.STOP_D = None
        self.STOP_S = None
        self.PALLE_P = None
        self.PALLE_R = None
        self.ASS = None
    def iter(self):
        return iter([self.nome_giocatore, self.numero_giocatore, self.squadra, self.ruolo, self.altezza,
                     self.minuti, self.FALLI_C, self.FALLI_S, self.T2_R, self.T2_T, self.T2_PER, self.T3_R,
                     self.T3_T, self.T3_PER, self.T1_R, self.T1_T, self.T1_PER, self.RIM_O, self.RIM_D,
                     self.RIM_T, self.STOP_D, self.STOP_S, self.PALLE_P, self.PALLE_R, self.ASS])

class ProfiloGiocatoreEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            return [self.default(profiloGiocatore) for profiloGiocatore in obj]
        elif isinstance(obj, ProfiloGiocatore):
            return {'nome_giocatore': obj.nome_giocatore,
                    'numero_giocatore': obj.numero_giocatore,
                    'squadra': obj.squadra,
                    'ruolo': obj.ruolo,
                    'altezza': obj.altezza,
                    'medie': obj.medie}