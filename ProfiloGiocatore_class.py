class ProfiloGiocatore:
    def __init__(self, nome_giocatore, numero_giocatore, squadra, ruolo, altezza):
        self.nome_giocatore = nome_giocatore
        self.numero_giocatore = numero_giocatore
        self.squadra = squadra
        self.ruolo = ruolo
        self.altezza = altezza
        self.minuti = 0.0
        self.FALLI_C = 0.0
        self.FALLI_S = 0.0
        self.T2_R = 0.0
        self.T2_T = 0.0
        self.T2_PER = self.percentuali(self.T2_R, self.T2_T)
        self.T3_R = 0.0
        self.T3_T = 0.0
        self.T3_PER = self.percentuali(self.T3_R, self.T3_T)
        self.T1_R = 0.0
        self.T1_T = 0.0
        self.T1_PER = self.percentuali(self.T1_R, self.T1_T)
        self.RIM_O = 0.0
        self.RIM_D = 0.0
        self.RIM_T = self.RIM_O + self.RIM_D
        self.STOP_D = 0.0
        self.STOP_S = 0.0
        self.PALLE_P = 0.0
        self.PALLE_R = 0.0
        self.ASS = 0.0
    def __iter__(self):
        return [self.nome_giocatore, self.numero_giocatore, self.squadra, self.ruolo, self.altezza,
                self.minuti, self.FALLI_C, self.FALLI_S, self.T2_R, self.T2_T, self.T2_PER, self.T3_R,
                self.T3_T, self.T3_PER, self.T1_R, self.T1_T, self.T1_PER, self.RIM_O, self.RIM_D,
                self.RIM_T, self.STOP_D, self.STOP_S, self.PALLE_P, self.PALLE_R, self.ASS]

    def percentuali(self, realizzati, tentati):
        if tentati != 0.0:
            return realizzati / tentati
        else:
            return 0.0

    def oer(self):
        return (self.T3_R+self.T2_R+self.T1_R)/self.po()
    def po(self):
        return self.T3_T+self.T2_T+(self.T1_T/2)+self.PALLE_P
    def der(self):
        return 1-self.oer()

#VIR = [(Punti fatti + AS * 1,5 + PR + SD * 0,75 + RO * 1,25 + RD * 0,75 + T3+/2 +FS/2 - FF/2 - ((T3-) + (T2-)) * 0,75 - PP - (TL-)/2) / Minuti giocati].

    def vir(self):
        return ((self.T3_R+self.T2_R+self.T1_R)+(self.ASS*1,5)+(self.PALLE_R)+(self.STOP_D*0,75)+(self.RIM_O)*1,25+(self.RIM_D*0,75)+(self.T3_R/2)+(self.FALLI_S/2)
                -(self.FALLI_C/2)-(self.T3_T-self.T3_R+self.T2_T-self.T2_R)*0,75 -self.PALLE_P-(self.T1_T-self.T1_R)/2)/self.minuti