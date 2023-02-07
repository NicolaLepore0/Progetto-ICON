/* Classe partita
 * 
 * Contiene i seguenti attributi:
 * - squadra_casa: nome della squadra casa
 * - squadra_ospite: nome della squadra ospite
 * - risultato_finale_host: risultato finale squadra casa
 * - risultato_finale_guest: risultato finale squadra ospite
 * - eventi: lista ordinata che contiene tutti gli eventi della partita
 */
:- dynamic giocatore/2.
:- dynamic entra_giocatore/2.
:- dynamic esce_giocatore/2.

    entra_giocatore(Giocatore, Squadra) :-
        not(giocatore(Giocatore, Squadra)),
        assertz(giocatore(Giocatore, Squadra)).

    esce_giocatore(Giocatore, Squadra) :-
        giocatore(Giocatore, Squadra),
        retract(giocatore(Giocatore, Squadra)).

    gestisci_giocatore(Giocatore, Squadra) :-
        (giocatore(Giocatore, Squadra) -> esce_giocatore(Giocatore, Squadra); entra_giocatore(Giocatore, Squadra)).

    giocatori_in_campo(Squadra) :-
        findall(Giocatore, giocatore(Giocatore, Squadra), Giocatori),
        write(Giocatori).

    squadra_giocatore(Giocatore, Squadra) :-
    giocatore(Giocatore, Squadra).

