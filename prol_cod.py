from pyswip import Prolog
import csv
import re

char_to_replace = {
    ' ': '_', '-': '_', '\'': '_', '&': 'and',
    'á': 'a', 'â': 'a', 'ã': 'a', 'ă': 'a', 'ă': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae', 'ą': 'a', 'à': 'a',
    'č': 'c', 'ć': 'c', 'ç': 'c',
    'đ': 'd',
    'é': 'e', 'ë': 'e', 'ę': 'e', 'è': 'e',
    'ğ': 'g',
    'ï': 'i', 'í': 'i', 'ı': 'i', 'î': 'i', 'ī': 'i',
    'ł': 'l',
    'ñ': 'n', 'ń': 'n',
    'ö': 'o', 'ó': 'o', 'ò': 'o', 'ô': 'o', 'ø': 'o',
    'ř': 'r',
    'ş': 's', 'ș': 's', 'š': 's',
    'þ': 'th',
    'ü': 'u', 'ú': 'u', 'ü': 'u',
    'ý': 'y',
    'ž': 'z', 'ż': 'z',
}

col_to_rem = [
    'numero_giocatore',
    'rim_o',
    'rim_d',
    't1_per',
    't2_per',
    't3_per',
    'ass',
]


def filter_bad_strings(value: str, char_to_replace: dict) -> str:
    to_replace = re.search("^[0-9]+[.]*_* *", value)
    if to_replace is not None:
        to_replace = to_replace.group(0)
        value = (value.replace(to_replace, '')) + '_' + (to_replace.strip())
    value = value.lower().replace('i̇', 'i').replace(' ', '_').replace('.', '')
    value = value.translate(str.maketrans(char_to_replace))
    return value

pl_kb = []

with open('dataset/giocatori_corretti.csv', 'r', encoding='utf-8') as f:
    csvr = csv.reader(f, delimiter=',')
    header = next(csvr)
    for i, player in enumerate(csvr):
        j = 0
        for h in header:
            if h not in col_to_rem:
                pred = ''
                value = ''
                pred = h
                value = player[j].lower().replace('i̇', 'i').replace(' ', '_')
                if j == 1:
                    value = re.sub("^[0-9]+[.]*_*", "", value)
                value = value.translate(str.maketrans(char_to_replace))
                pl_kb.append(f'{pred}({i + 1},{value}).')
            j += 1

    pl_kb.sort()

    #pl_kb.append("show_team(Team, Player) :- team(Id, Team), name(Id, Player)")
    #pl_kb.append("show_goal(_, [], [])")
    #pl_kb.append("show_goal(Threshold, [H | T], [[Name, N_goal] | T_res]) :- goals(H, N_goal), N_goal > Threshold, name(H, Name), show_goal(Threshold, T, T_res)")
    #pl_kb.append("show_goal(Threshold, [H | T], T_res) :- goals(H, N_goal), N_goal =< Threshold, show_goal(Threshold, T, T_res)")

    with open('dataset_preprocessed.pl', 'w', encoding='utf-8') as fout:
        for line in pl_kb:
            fout.write(line + "\n")

        with open('prolog.pl', 'r', encoding='utf-8') as f:
            for line in f:
                fout.write(line)

prolog = Prolog()
prolog.consult("dataset_preprocessed.pl")
list_ids = f"[{', '.join([str(x) for x in range(1, 5000)])}]"

# print("Playmaker: ")
pl_list = list(prolog.query(f"evaluate_all_play(Pl)"))[0]['Pl']
pl_list.sort(key=lambda row: row[1], reverse=True)
# for dc in dc_list:
#    print(dc)

# print("Centro: ")
cn_list = list(prolog.query(f"evaluate_all_centro(Cn)"))[0]['Cn']
cn_list.sort(key=lambda row: row[1], reverse=True)
# for fb in fb_list:
#    print(fb)

# print("Ala: ")
al_list = list(prolog.query(f"evaluate_all_ala(Al)"))[0]['Al']
al_list.sort(key=lambda row: row[1], reverse=True)
# for dm in dm_list:
#    print(dm)

# print("Guardia: ")
gd_list = list(prolog.query(f"evaluate_all_guardia(Gd)"))[0]['Gd']
gd_list.sort(key=lambda row: row[1], reverse=True)
# for mc in mc_list:
#    print(mc)

def comparePlayers(plList):
    p1 = input("Dammi il primo giocatore: ")
    p1Converted = p1
    p1Converted = p1Converted.replace(" ", "_")
    p1Converted = p1Converted.lower()
    p2 = input("Dammi il secondo giocatore: ")
    p2Converted = p2
    p2Converted = p2Converted.replace(" ", "_")
    p2Converted = p2Converted.lower()
    pl = []
    for x in plList:
        if(x[0] == p1Converted or x[0] == p2Converted):
            pl.append(x)
    else:
        percP1 = f'{pl[0][1] / (pl[0][1] + pl[1][1]) * 100:.2f} %'
        percP2 = f'{pl[1][1] / (pl[0][1] + pl[1][1]) * 100:.2f} %'
        print(f'{p1 if pl[0][0] == p1Converted else p2} {percP1} - {percP2} {p1 if pl[0][0] == p2Converted else p2}')

scelta = input("Cosa vuoi confrontare? (Pl/Cn/Al/Gd): ")
if scelta == 'Pl':
    comparePlayers(pl_list)
elif scelta == 'Cn':
    comparePlayers(cn_list)
elif scelta == 'Al':
    comparePlayers(al_list)
elif scelta == 'Gd':
    comparePlayers(gd_list)
