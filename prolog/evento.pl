/* Classe evento
 * 
 * Contiene i seguenti attributi:
 * - punti_casa: contiene i punti della squadra di casa attuali
 * - punti_ospite: contiene i punti della squadra ospite attuali
 * - evento: tipologia di evento
 * - quarto: indica il quarto che si sta giocando
 * - time: indica il tempo mancante alla fine del quarto
 * - giocatore: nome giocatore che ha compiuto l'evento
 */
punti_casa(P) :- P.
punti_ospite(P) :- P.
evento(E) :- E.
quarto(Q) :- Q.
time(T) :- T.

giocatore_in_campo(NomeGiocatore) :- evento_compiuto(NomeGiocatore).

giocatore_fuori_campo(Nome_giocatore) :- not giocatore_in_campo(NomeGiocatore).
giocatore_in_campo(Nome_giocatore) :- not giocatore_fuori_campo(NomeGiocatore).

fuori_campo(Giocatore) :- falli(Giocatore, NumFalli), NumFalli >= 5.

vincitore(Casa, Ospite, 'casa') :- Casa > Ospite.
vincitore(Casa, Ospite, 'ospite') :- Casa < Ospite.
vincitore(Casa, Ospite, 'pareggio') :- Casa = Ospite.

giocatore(NomeGiocatore).
punti_fatti_da(NomeGiocatore, Punti).

miglior_realizzatore(NomeGiocatore, NumeroMaglia, Squadra, Punti) :-
punti_fatti_da(NomeGiocatore, Punti), giocatore(NomeGiocatore, NumeroMaglia, Squadra),
not( (punti_fatti_da(NomeGiocatoreAltro, PuntiAltri), giocatore(NomeGiocatoreAltro, _, _), PuntiAltri > Punti) ).ù
