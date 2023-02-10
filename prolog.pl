handleDivisionByZero(X1, X2, Y) :-
    X2 > 0,
    Y is X1 / X2.
handleDivisionByZero(X1, X2, Y) :-
    X2 < 0,
    Y is X1 / X2.
handleDivisionByZero(_, X2, Y) :-
    X2 = 0,
    Y is 0.

calc_max([], R, R). %end
calc_max([X|Xs], WK, R):- X >  WK, calc_max(Xs, X, R). %WK is Carry about
calc_max([X|Xs], WK, R):- X =< WK, calc_max(Xs, WK, R).
calc_max([X|Xs], R):- calc_max(Xs,X,R).%start

is_centro(Id) :- role(Id,g). %play è un ruolo
is_ala(Id) :- role(Id,g).
is_centro(Id) :- role(Id,g).
is_guardia(Id) :- role(Id,g).

%Altezze
get_all_height([], []).
get_all_height([H | T], Res_list) :-
    altezza(H, Res),
    get_all_height(T, Res_down),
    append([Res], Res_down,Res_list).

%Minuti
get_all_minutesPlayed([], []).
get_all_minutesPlayed([H | T], Res_list) :-
    minuti(H, Res),
    get_all_minutesPlayed(T, Res_down),
    append([Res], Res_down,Res_list).

%Falli subiti
get_all_fouls_s([], []).
get_all_fouls_s([H | T], Res_list) :-
    fouls_s(H, Res),
    get_all_fouls_s(T, Res_down),
    append([Res], Res_down,Res_list).

%Falli commessi
get_all_fouls_c([], []).
get_all_fouls_c([H | T], Res_list) :-
    fouls_c(H, Res),
    get_all_fouls_c(T, Res_down),
    append([Res], Res_down,Res_list).

%Tiri 2 risuciti
get_all_T2([], []).
get_all_T2([H | T], Res_list) :-
    t2(H, Res),
    get_all_T2(T, Res_down),
    append([Res], Res_down,Res_list).

%Tiri 2 tentati
get_all_T2T([], []).
get_all_T2T([H | T], Res_list) :-
    t2t(H, Res),
    get_all_T2T(T, Res_down),
    append([Res], Res_down,Res_list).

%Tiri 3 risuciti
get_all_T3([], []).
get_all_T3([H | T], Res_list) :-
    t3(H, Res),
    get_all_T3(T, Res_down),
    append([Res], Res_down,Res_list).

%Tiri 3 tentati
get_all_T3T([], []).
get_all_T3T([H | T], Res_list) :-
    t3t(H, Res),
    get_all_T3T(T, Res_down),
    append([Res], Res_down,Res_list).

%Tiri 1 risuciti
get_all_T1([], []).
get_all_T1([H | T], Res_list) :-
    t1(H, Res),
    get_all_T1(T, Res_down),
    append([Res], Res_down,Res_list).

%Tiri 1 tentati
get_all_T1T([], []).
get_all_T1T([H | T], Res_list) :-
    t1t(H, Res),
    get_all_T1T(T, Res_down),
    append([Res], Res_down,Res_list).

%Rimbalzi T
get_all_rebaunds([], []).
get_all_rebaunds([H | T], Res_list) :-
    rebaunds(H, Res),
    get_all_rebaunds(T, Res_down),
    append([Res], Res_down,Res_list).

%Stoppate Date
get_all_stopD([], []).
get_all_stopD([H | T], Res_list) :-
    stopD(H, Res),
    get_all_stopD(T, Res_down),
    append([Res], Res_down,Res_list).

%Stoppate Subite
get_all_stoS([], []).
get_all_stopS([H | T], Res_list) :-
    stopS(H, Res),
    get_all_stopS(T, Res_down),
    append([Res], Res_down,Res_list).

%Palle perse
get_all_palleP([], []).
get_all_palleP([H | T], Res_list) :-
    palleP(H, Res),
    get_all_palleP(T, Res_down),
    append([Res], Res_down,Res_list).

%Palle recuperate
get_all_palleR([], []).
get_all_palleR([H | T], Res_list) :-
    palleR(H, Res),
    get_all_palleR(T, Res_down),
    append([Res], Res_down,Res_list).

%Percentuale T2
t2Percentage(Id, T2Percentage) :-
    t2(Id, T2),
    t2T(Id, T2T),
    handleDivisionByZero(T2, T2T, Y),
    T2Percentage is Y.

%Percentuale T3
t3Percentage(Id, T3Percentage) :-
    t3(Id, T3),
    t3T(Id, T3T),
    handleDivisionByZero(T3, T3T, Y),
    T3Percentage is Y.

%Percentuale T1
t1Percentage(Id, T1Percentage) :-
    t1(Id, T1),
    t1T(Id, T1T),
    handleDivisionByZero(T1, T1T, Y),
    T1Percentage is Y.

%Da una valutazione sull'altezza dei giocatori
eval_height(Height, Lower_bound, _, _, _, _, Eval) :-
    Height =< Lower_bound,
    Eval is 0.
eval_height(Height, Lower_bound, Upper_bound, Perc_lower, _, Max, Eval) :-
    Height > Lower_bound,
    Height =< Upper_bound,
    Eval is Height / Max * Perc_lower.
eval_height(Height, _, Upper_bound, _, Perc_upper, Max, Eval) :-
    Height > Upper_bound,
    Eval is Height / Max*Perc_upper.

%Da una valutazione sui minuti giocati
eval_mp(MinutesPlayed, Min_mp1, _, Perc1, _, _, Max, Eval) :-
    MinutesPlayed < Min_mp1,
    Eval is MinutesPlayed / Max * Perc1.
eval_mp(MinutesPlayed, Min_mp1, Min_mp2, _, Perc2, _, Max, Eval) :-
    MinutesPlayed >= Min_mp1,
    MinutesPlayed < Min_mp2,
    Eval is Min_mp2 / Max * Perc2.
eval_mp(MinutesPlayed, _, Min_mp2, _, _, Perc3, Max, Eval) :-
    MinutesPlayed >= Min_mp2,
    Eval is Min_mp2/Max*Perc3.

%Valutazione percentuale da 2
eval_t2Percentage(T2Percentage, T2T, Threshold, Perc, Eval) :-
    T2T < Threshold,
    Eval is T2Percentage * Perc.
eval_t2Percentage(T2Percentage, T2T, Threshold, _, Eval) :-
    T2T >= Threshold,
    Eval is T2Percentage.

%Valutazione percentuale da 3
eval_t3Percentage(T3Percentage, T3T, Threshold, Perc, Eval) :-
    T3T < Threshold,
    Eval is T3Percentage * Perc.
eval_t3Percentage(T3Percentage, T3T, Threshold, _, Eval) :-
    T3T >= Threshold,
    Eval is T3Percentage.

%Valutazione percentuale da 1
eval_t1Percentage(T1Percentage, T1T, Threshold, Perc, Eval) :-
    T1T < Threshold,
    Eval is T1Percentage * Perc.
eval_t1Percentage(T1Percentage, T1T, Threshold, _, Eval) :-
    T1T >= Threshold,
    Eval is T1Percentage.


evaluate_all_centro(Pl) :-
    findall(Player, is_centro(Player), Players),

    get_all_height(Players, Height_list),
    get_all_minutesPlayed(Players, MinutesPlayed_list),
    get_all_fouls_c(Players, Fouls_c_list),
    get_all_fouls_s(Players, Fouls_s_list),
    get_all_T2(Players, T2_list),
    get_all_T2T(Players, T2T_list),
    get_all_T3(Players, T3_list),
    get_all_T3T(Players, T3T_list),
    get_all_T1(Players, T1_list),
    get_all_T1T(Players, T1T_list),
    get_all_rebaunds(Players, Rebaunds_list),
    get_all_stopD(Players, StopD_list),
    get_all_stopS(Players, StopS_list),
    get_all_palleP(Players, PalleP_list),
    get_all_palleR(Players, PalleR_list),

    calc_max(Height_list, Max_height),
    calc_max(MinutesPlayed_list, Max_minutesPlayed),
    calc_max(Fouls_c_list, Max_Fouls_c),
    calc_max(Fouls_s_list, Max_Fouls_s),
    calc_max(T2_list, Max_T2),
    calc_max(T2T_list, Max_T2T),
    calc_max(T3_list, Max_T3),
    calc_max(T3T_list, Max_T3T),
    calc_max(T1_list, Max_T1),
    calc_max(T1T_list, Max_T1T),
    calc_max(Rebaunds_list, Max_Rebaunds),
    calc_max(StopD_list, Max_StopD),
    calc_max(StopS_list, Max_StopS),
    calc_max(PalleP_list, Max_PalleP),
    calc_max(PalleR_list, Max_PalleR),

    evaluate_all_Pl(Players,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Pl).

evaluate_all_Pl([],  _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, []).
evaluate_all_Pl([H | T],
            Max_height,
            Max_minutesPlayed,
            Max_Fouls_c,
            Max_Fouls_s,
            Max_T2,
            Max_T2T,
            Max_T3,
            Max_T3T,
            Max_T1,
            Max_T1T,
            Max_Rebaunds,
            Max_StopD,
            Max_StopS,
            Max_PalleP,
            Max_PalleR,
            Res) :-
    evaluation_Pl(H,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_local),
    evaluate_all_Pl(T,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_down),
    %%%%%% da modificare
    name(H, Name),
    append([[Name, Eval_local]], Eval_down, Res).

evaluation_Pl(Id,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval) :-
    is_centro(Id),
    altezza(Id, Height),
    eval_height(Height, 176, 182, 0.4, 0.6, Max_height, Eval_height),
    altezza(Id, Height),
    minuti(Id, MinutesPlayed),
    fouls_c(Id,Fouls_c),
    fouls_s(Id,Fouls_s),
    t2(Id,T2),
    t2T(Id,T2T),
    t3(Id,T3),
    t3T(Id,T3T),
    t1(Id,T1),
    t1T(Id,T1T),
    rebaunds(Id,Rebaunds),
    stopD(Id,StopD),
    stopS(Id,StopS),
    palleP(Id,PalleP),
    palleR(Id,PalleR),

    handleDivisionByZero(MinutesPlayed, Max_minutesPlayed, MinutesPlayed_divided)
    handleDivisionByZero(Fouls_c, Max_Fouls_c, Fouls_c_divided)
    handleDivisionByZero(Fouls_s, Max_Fouls_s, Max_Fouls_s_divided)
    handleDivisionByZero(T2, Max_T2, T2_divided)
    handleDivisionByZero(T2T, Max_T2T, T2T_divided)
    handleDivisionByZero(T3, Max_T3, T3_divided)
    handleDivisionByZero(T3T, Max_T3T, T3T_divided)
    handleDivisionByZero(T1, Max_T1, T1_divided)
    handleDivisionByZero(T1T, Max_T1T, T1T_divided)
    handleDivisionByZero(Rebaunds, Max_Rebaunds, Rebaunds_divided)
    handleDivisionByZero(StopD, Max_StopD, StopD_divided)
    handleDivisionByZero(StopS, Max_StopS, StopS_divided)
    handleDivisionByZero(PalleP, Max_PalleP, PalleP_divided)
    handleDivisionByZero(PalleR, Max_PalleR, PalleR_divided)

    Eval is
        Eval_height +
        (Fouls_c *0,5 +
        Fouls_s *0,5 +
        T2 *1 +
        (T2T - T2) *0,75 +
        T3 *1 +
        (T3T - T3) *0,75 +
        T1 +
        (T1T - T1) *0,5 +
        Rebaunds *1 +
        StopD *0,75 +
        StopS *0,2 +
        PalleP *1 +
        PalleR *1
        ) / MinutesPlayed * Eval_mp.


evaluate_all_centro(Cn) :-
    findall(Player, is_centro(Player), Players),

    get_all_height(Players, Height_list),
    get_all_minutesPlayed(Players, MinutesPlayed_list),
    get_all_fouls_c(Players, Fouls_c_list),
    get_all_fouls_s(Players, Fouls_s_list),
    get_all_T2(Players, T2_list),
    get_all_T2T(Players, T2T_list),
    get_all_T3(Players, T3_list),
    get_all_T3T(Players, T3T_list),
    get_all_T1(Players, T1_list),
    get_all_T1T(Players, T1T_list),
    get_all_rebaunds(Players, Rebaunds_list),
    get_all_stopD(Players, StopD_list),
    get_all_stopS(Players, StopS_list),
    get_all_palleP(Players, PalleP_list),
    get_all_palleR(Players, PalleR_list),

    calc_max(Height_list, Max_height),
    calc_max(MinutesPlayed_list, Max_minutesPlayed),
    calc_max(Fouls_c_list, Max_Fouls_c),
    calc_max(Fouls_s_list, Max_Fouls_s),
    calc_max(T2_list, Max_T2),
    calc_max(T2T_list, Max_T2T),
    calc_max(T3_list, Max_T3),
    calc_max(T3T_list, Max_T3T),
    calc_max(T1_list, Max_T1),
    calc_max(T1T_list, Max_T1T),
    calc_max(Rebaunds_list, Max_Rebaunds),
    calc_max(StopD_list, Max_StopD),
    calc_max(StopS_list, Max_StopS),
    calc_max(PalleP_list, Max_PalleP),
    calc_max(PalleR_list, Max_PalleR),

    evaluate_all_Cn(Players,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Cn).

evaluate_all_Cn([],  _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, []).
evaluate_all_Cn([H | T],
            Max_height,
            Max_minutesPlayed,
            Max_Fouls_c,
            Max_Fouls_s,
            Max_T2,
            Max_T2T,
            Max_T3,
            Max_T3T,
            Max_T1,
            Max_T1T,
            Max_Rebaunds,
            Max_StopD,
            Max_StopS,
            Max_PalleP,
            Max_PalleR,
            Res) :-
    evaluation_Cn(H,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_local),
    evaluate_all_Cn(T,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_down),
    %%%%%% da modificare
    name(H, Name),
    append([[Name, Eval_local]], Eval_down, Res).

evaluation_Cn(Id,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval) :-
    is_centro(Id),
    altezza(Id, Height),
    eval_height(Height, 176, 182, 0.4, 0.6, Max_height, Eval_height),
    altezza(Id, Height),
    minuti(Id, MinutesPlayed),
    fouls_c(Id,Fouls_c),
    fouls_s(Id,Fouls_s),
    t2(Id,T2),
    t2T(Id,T2T),
    t3(Id,T3),
    t3T(Id,T3T),
    t1(Id,T1),
    t1T(Id,T1T),
    rebaunds(Id,Rebaunds),
    stopD(Id,StopD),
    stopS(Id,StopS),
    palleP(Id,PalleP),
    palleR(Id,PalleR),

    handleDivisionByZero(MinutesPlayed, Max_minutesPlayed, MinutesPlayed_divided)
    handleDivisionByZero(Fouls_c, Max_Fouls_c, Fouls_c_divided)
    handleDivisionByZero(Fouls_s, Max_Fouls_s, Max_Fouls_s_divided)
    handleDivisionByZero(T2, Max_T2, T2_divided)
    handleDivisionByZero(T2T, Max_T2T, T2T_divided)
    handleDivisionByZero(T3, Max_T3, T3_divided)
    handleDivisionByZero(T3T, Max_T3T, T3T_divided)
    handleDivisionByZero(T1, Max_T1, T1_divided)
    handleDivisionByZero(T1T, Max_T1T, T1T_divided)
    handleDivisionByZero(Rebaunds, Max_Rebaunds, Rebaunds_divided)
    handleDivisionByZero(StopD, Max_StopD, StopD_divided)
    handleDivisionByZero(StopS, Max_StopS, StopS_divided)
    handleDivisionByZero(PalleP, Max_PalleP, PalleP_divided)
    handleDivisionByZero(PalleR, Max_PalleR, PalleR_divided)

    Eval is
        Eval_height +
        (Fouls_c *0,5 +
        Fouls_s *0,5 +
        T2 *1 +
        (T2T - T2) *0,75 +
        T3 *1 +
        (T3T - T3) *0,75 +
        T1 +
        (T1T - T1) *0,5 +
        Rebaunds *1 +
        StopD *0,75 +
        StopS *0,2 +
        PalleP *1 +
        PalleR *1
        ) / MinutesPlayed * Eval_mp.

evaluate_all_guardia(Gd) :-
    findall(Player, is_guardia(Player), Players),

    get_all_height(Players, Height_list),
    get_all_minutesPlayed(Players, MinutesPlayed_list),
    get_all_fouls_c(Players, Fouls_c_list),
    get_all_fouls_s(Players, Fouls_s_list),
    get_all_T2(Players, T2_list),
    get_all_T2T(Players, T2T_list),
    get_all_T3(Players, T3_list),
    get_all_T3T(Players, T3T_list),
    get_all_T1(Players, T1_list),
    get_all_T1T(Players, T1T_list),
    get_all_rebaunds(Players, Rebaunds_list),
    get_all_stopD(Players, StopD_list),
    get_all_stopS(Players, StopS_list),
    get_all_palleP(Players, PalleP_list),
    get_all_palleR(Players, PalleR_list),

    calc_max(Height_list, Max_height),
    calc_max(MinutesPlayed_list, Max_minutesPlayed),
    calc_max(Fouls_c_list, Max_Fouls_c),
    calc_max(Fouls_s_list, Max_Fouls_s),
    calc_max(T2_list, Max_T2),
    calc_max(T2T_list, Max_T2T),
    calc_max(T3_list, Max_T3),
    calc_max(T3T_list, Max_T3T),
    calc_max(T1_list, Max_T1),
    calc_max(T1T_list, Max_T1T),
    calc_max(Rebaunds_list, Max_Rebaunds),
    calc_max(StopD_list, Max_StopD),
    calc_max(StopS_list, Max_StopS),
    calc_max(PalleP_list, Max_PalleP),
    calc_max(PalleR_list, Max_PalleR),

    evaluate_all_Gd(Players,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Gd).

evaluate_all_Gd([],  _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, []).
evaluate_all_Gd([H | T],
            Max_height,
            Max_minutesPlayed,
            Max_Fouls_c,
            Max_Fouls_s,
            Max_T2,
            Max_T2T,
            Max_T3,
            Max_T3T,
            Max_T1,
            Max_T1T,
            Max_Rebaunds,
            Max_StopD,
            Max_StopS,
            Max_PalleP,
            Max_PalleR,
            Res) :-
    evaluation_Gd(H,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_local),
    evaluate_all_Gd(T,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_down),
    %%%%%% da modificare
    name(H, Name),
    append([[Name, Eval_local]], Eval_down, Res).

evaluation_Gd(Id,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval) :-
    is_guardia(Id),
    altezza(Id, Height),
    eval_height(Height, 176, 182, 0.4, 0.6, Max_height, Eval_height),
    altezza(Id, Height),
    minuti(Id, MinutesPlayed),
    fouls_c(Id,Fouls_c),
    fouls_s(Id,Fouls_s),
    t2(Id,T2),
    t2T(Id,T2T),
    t3(Id,T3),
    t3T(Id,T3T),
    t1(Id,T1),
    t1T(Id,T1T),
    rebaunds(Id,Rebaunds),
    stopD(Id,StopD),
    stopS(Id,StopS),
    palleP(Id,PalleP),
    palleR(Id,PalleR),

    handleDivisionByZero(MinutesPlayed, Max_minutesPlayed, MinutesPlayed_divided)
    handleDivisionByZero(Fouls_c, Max_Fouls_c, Fouls_c_divided)
    handleDivisionByZero(Fouls_s, Max_Fouls_s, Max_Fouls_s_divided)
    handleDivisionByZero(T2, Max_T2, T2_divided)
    handleDivisionByZero(T2T, Max_T2T, T2T_divided)
    handleDivisionByZero(T3, Max_T3, T3_divided)
    handleDivisionByZero(T3T, Max_T3T, T3T_divided)
    handleDivisionByZero(T1, Max_T1, T1_divided)
    handleDivisionByZero(T1T, Max_T1T, T1T_divided)
    handleDivisionByZero(Rebaunds, Max_Rebaunds, Rebaunds_divided)
    handleDivisionByZero(StopD, Max_StopD, StopD_divided)
    handleDivisionByZero(StopS, Max_StopS, StopS_divided)
    handleDivisionByZero(PalleP, Max_PalleP, PalleP_divided)
    handleDivisionByZero(PalleR, Max_PalleR, PalleR_divided)

    Eval is
        Eval_height +
        (Fouls_c *0,5 +
        Fouls_s *0,5 +
        T2 *1 +
        (T2T - T2) *0,75 +
        T3 *1 +
        (T3T - T3) *0,75 +
        T1 +
        (T1T - T1) *0,5 +
        Rebaunds *1 +
        StopD *0,75 +
        StopS *0,2 +
        PalleP *1 +
        PalleR *1
        ) / MinutesPlayed * Eval_mp.

evaluate_all_ala(Al) :-
    findall(Player, is_ala(Player), Players),

    get_all_height(Players, Height_list),
    get_all_minutesPlayed(Players, MinutesPlayed_list),
    get_all_fouls_c(Players, Fouls_c_list),
    get_all_fouls_s(Players, Fouls_s_list),
    get_all_T2(Players, T2_list),
    get_all_T2T(Players, T2T_list),
    get_all_T3(Players, T3_list),
    get_all_T3T(Players, T3T_list),
    get_all_T1(Players, T1_list),
    get_all_T1T(Players, T1T_list),
    get_all_rebaunds(Players, Rebaunds_list),
    get_all_stopD(Players, StopD_list),
    get_all_stopS(Players, StopS_list),
    get_all_palleP(Players, PalleP_list),
    get_all_palleR(Players, PalleR_list),

    calc_max(Height_list, Max_height),
    calc_max(MinutesPlayed_list, Max_minutesPlayed),
    calc_max(Fouls_c_list, Max_Fouls_c),
    calc_max(Fouls_s_list, Max_Fouls_s),
    calc_max(T2_list, Max_T2),
    calc_max(T2T_list, Max_T2T),
    calc_max(T3_list, Max_T3),
    calc_max(T3T_list, Max_T3T),
    calc_max(T1_list, Max_T1),
    calc_max(T1T_list, Max_T1T),
    calc_max(Rebaunds_list, Max_Rebaunds),
    calc_max(StopD_list, Max_StopD),
    calc_max(StopS_list, Max_StopS),
    calc_max(PalleP_list, Max_PalleP),
    calc_max(PalleR_list, Max_PalleR),

    evaluate_all_Al(Players,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Al).

evaluate_all_Al([],  _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, []).
evaluate_all_Al([H | T],
            Max_height,
            Max_minutesPlayed,
            Max_Fouls_c,
            Max_Fouls_s,
            Max_T2,
            Max_T2T,
            Max_T3,
            Max_T3T,
            Max_T1,
            Max_T1T,
            Max_Rebaunds,
            Max_StopD,
            Max_StopS,
            Max_PalleP,
            Max_PalleR,
            Res) :-
    evaluation_Pl(H,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_local),
    evaluate_all_Pl(T,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval_down),
    %%%%%% da modificare
    name(H, Name),
    append([[Name, Eval_local]], Eval_down, Res).

evaluation_Pl(Id,
        Max_height,
        Max_minutesPlayed,
        Max_Fouls_c,
        Max_Fouls_s,
        Max_T2,
        Max_T2T,
        Max_T3,
        Max_T3T,
        Max_T1,
        Max_T1T,
        Max_Rebaunds,
        Max_StopD,
        Max_StopS,
        Max_PalleP,
        Max_PalleR,
        Eval) :-
    is_ala(Id),
    altezza(Id, Height),
    eval_height(Height, 176, 182, 0.4, 0.6, Max_height, Eval_height),
    altezza(Id, Height),
    minuti(Id, MinutesPlayed),
    fouls_c(Id,Fouls_c),
    fouls_s(Id,Fouls_s),
    t2(Id,T2),
    t2T(Id,T2T),
    t3(Id,T3),
    t3T(Id,T3T),
    t1(Id,T1),
    t1T(Id,T1T),
    rebaunds(Id,Rebaunds),
    stopD(Id,StopD),
    stopS(Id,StopS),
    palleP(Id,PalleP),
    palleR(Id,PalleR),

    handleDivisionByZero(MinutesPlayed, Max_minutesPlayed, MinutesPlayed_divided)
    handleDivisionByZero(Fouls_c, Max_Fouls_c, Fouls_c_divided)
    handleDivisionByZero(Fouls_s, Max_Fouls_s, Max_Fouls_s_divided)
    handleDivisionByZero(T2, Max_T2, T2_divided)
    handleDivisionByZero(T2T, Max_T2T, T2T_divided)
    handleDivisionByZero(T3, Max_T3, T3_divided)
    handleDivisionByZero(T3T, Max_T3T, T3T_divided)
    handleDivisionByZero(T1, Max_T1, T1_divided)
    handleDivisionByZero(T1T, Max_T1T, T1T_divided)
    handleDivisionByZero(Rebaunds, Max_Rebaunds, Rebaunds_divided)
    handleDivisionByZero(StopD, Max_StopD, StopD_divided)
    handleDivisionByZero(StopS, Max_StopS, StopS_divided)
    handleDivisionByZero(PalleP, Max_PalleP, PalleP_divided)
    handleDivisionByZero(PalleR, Max_PalleR, PalleR_divided)

    Eval is
        Eval_height +
        (Fouls_c *0,5 +
        Fouls_s *0,5 +
        T2 *1 +
        (T2T - T2) *0,75 +
        T3 *1 +
        (T3T - T3) *0,75 +
        T1 +
        (T1T - T1) *0,5 +
        Rebaunds *1 +
        StopD *0,75 +
        StopS *0,2 +
        PalleP *1 +
        PalleR *1
        ) / MinutesPlayed * Eval_mp.





