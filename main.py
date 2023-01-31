
from pyswip import Prolog

class KnowledgeBase():

    def __init__(self, syncro):
        '''
        Metodo init
        ---------------
        Inizializza il motore di prolog e gli algoritmi di machine learning
        ----------------
        Dati di input
        --------------
        syncro: booleano che indica se sincronizzare i semafori
        '''
        self.prolog = Prolog()
        self.prolog.consult("prolog/KB.pl",catcherrors=False)

