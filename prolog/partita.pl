/* Classe partita
 * 
 * Contiene i seguenti attributi:
 * - squadra_casa: nome della squadra casa
 * - squadra_ospite: nome della squadra ospite
 * - risultato_finale_host: risultato finale squadra casa
 * - risultato_finale_guest: risultato finale squadra ospite
 * - eventi: lista ordinata che contiene tutti gli eventi della partita
 */

primi_cinque_usciti(Eventi, GiocatoriUsciti) :-
    trova_uscite(Eventi, [], 0, GiocatoriUsciti),
    length(GiocatoriUsciti, NumeroUsciti),
    NumeroUsciti == 5.

trova_uscite([], GiocatoriUsciti, 5, GiocatoriUsciti).
trova_uscite([evento(NomeGiocatore, uscita) | EventiRestanti], GiocatoriEntrati, ContatoreUsciti, GiocatoriUsciti) :-
    \+ member(NomeGiocatore, GiocatoriEntrati),
    ContatoreUsciti < 5,
    ContatoreUscitoSuccessivo is ContatoreUsciti + 1,
    trova_uscite(EventiRestanti, GiocatoriEntrati, ContatoreUscitoSuccessivo, GiocatoriUscitiSuccessivi),
    GiocatoriUsciti = [NomeGiocatore | GiocatoriUscitiSuccessivi].
trova_uscite([evento(NomeGiocatore, entrata) | EventiRestanti], GiocatoriEntrati, ContatoreUsciti, GiocatoriUsciti) :-
    trova_uscite(EventiRestanti, [NomeGiocatore | GiocatoriEntrati], ContatoreUsciti, GiocatoriUsciti).



titolari_ospite():-
quintetto_casa(Giocatore1, Giocatore2, Giocatore3, Giocatore4, Giocatore5) :-
    ingresso(Giocatore1),ingresso(Giocatore2),ingresso(Giocatore3),ingresso(Giocatore4),ingresso(Giocatore5),
    not(uscita(Giocatore1),uscita(Giocatore2),uscita(Giocatore3),uscita(Giocatore4),uscita(Giocatore5)).

quintetto_ospite(Giocatore1, Giocatore2, Giocatore3, Giocatore4, Giocatore5) :-
    ingresso(Giocatore1),ingresso(Giocatore2),ingresso(Giocatore3),ingresso(Giocatore4),ingresso(Giocatore5),
    not(uscita(Giocatore1),uscita(Giocatore2),uscita(Giocatore3),uscita(Giocatore4),uscita(Giocatore5)).



