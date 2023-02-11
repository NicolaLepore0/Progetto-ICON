from pyswip import Prolog
import csv
import re

char_to_replace = {
    ' ': '_', '-': '', '\'': '_', '&': 'and',
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
                value = player[j].lower().replace(' ', '_')
                if j == 1:
                    value = re.sub("^[0-9]+[.]*_*", "", value)
                value = value.translate(str.maketrans(char_to_replace))
                pl_kb.append(f'{pred}({i + 1},{value}).')
            j += 1

    pl_kb.sort()

    with open('dataset_preprocessed.pl', 'w', encoding='utf-8') as fout:
        for line in pl_kb:
            fout.write(line + "\n")

        with open('prolog.pl', 'r', encoding='utf-8') as f:
            for line in f:
                fout.write(line)

prolog = Prolog()
prolog.consult("dataset_preprocessed.pl")
list_ids = f"[{', '.join([str(x) for x in range(1, 2000)])}]"

pl_list = list(prolog.query(f"evaluate_all_pl(Pl)"))[0]["Pl"]
pl_list.sort(key=lambda row: row[1], reverse=True)
for pl in pl_list:
    print(pl[0])

# print("Centro: ")
cn_list = list(prolog.query(f"evaluate_all_cn(Cn)"))[0]["Cn"]
cn_list.sort(key=lambda row: row[1], reverse=True)


# print("Ala: ")
al_list = list(prolog.query(f"evaluate_all_al(Al)"))[0]["Al"]
al_list.sort(key=lambda row: row[1], reverse=True)
# for dm in dm_list:
#    print(dm)

# print("Guardia: ")
gd_list = list(prolog.query(f"evaluate_all_gd(Gd)"))[0]["Gd"]
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
        if(str(x[0]) == p1Converted  or str(x[0]) == p2Converted):
            pl.append(x)
            print(x)
    percP1 = f'{pl[0][1] / (pl[0][1] + pl[1][1]) * 100:.2f} %'
    percP2 = f'{pl[1][1] / (pl[0][1] + pl[1][1]) * 100:.2f} %'
    print(f'{str(p1) if pl[0][0] == p1Converted else str(p2)} {percP1} - {percP2} {str(p2) if pl[0][0] == p2Converted else str(p1)}')

scelta = input("Cosa vuoi confrontare? (pl/cn/al/gd): ")
if scelta == 'pl':
    comparePlayers(pl_list)
elif scelta == 'cn':
    comparePlayers(cn_list)
elif scelta == 'al':
    comparePlayers(al_list)
elif scelta == 'gd':
    comparePlayers(gd_list)
