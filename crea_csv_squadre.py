import json

with open("dataset/squadre.txt", "r") as file:
    lista = [riga.strip() for riga in file]
print(lista)

with open("dataset/partita.json", "r") as file:
    data = json.load(file)

for squadra in lista:
    n_partite = 0

    casa_puntiFatti = 0
    casa_puntiSubiti = 0
    casa_falliFatti = 0
    casa_falliSubiti = 0
    casa_pallePerse = 0
    casa_palleRecuperate = 0
    casa_t2_r = 0
    casa_t2_s = 0
    casa_t3_r = 0
    casa_t3_s = 0
    casa_t1_r = 0
    casa_t1_s = 0
    casa_rimbalzi = 0

    ospiti_puntiFatti = 0
    ospiti_puntiSubiti = 0
    ospiti_falliFatti = 0
    ospiti_falliSubiti = 0
    ospiti_pallePerse = 0
    ospiti_palleRecuperate = 0
    ospiti_t2_r = 0
    ospiti_t2_s = 0
    ospiti_t3_r = 0
    ospiti_t3_s = 0
    ospiti_t1_r = 0
    ospiti_t1_s = 0
    ospiti_rimbalzi = 0

    for partita in data:
        if partita['squadra_casa'] == squadra and len(partita['eventi']) > 0:
            print(partita['eventi'][0]['evento'])
            casa_puntiFatti = casa_puntiFatti + int(partita['risultato_finale_host'])
            casa_puntiSubiti = casa_puntiSubiti + int(partita['risultato_finale_guest'])
            i = 0
            while i < len(partita.eventi):
                if partita.eventi[i].giocatore:
                    if partita['eventi'][i]['evento'] == "FF":
                        casa_falliFatti = casa_falliFatti + 1
                    elif partita['eventi'][i]['evento'] == "FS":
                        casa_falliSubiti = casa_falliSubiti + 1
                    elif partita['eventi'][i]['evento'] == "PP":
                        casa_pallePerse = casa_pallePerse + 1
                    elif partita['eventi'][i]['evento'] == "PR":
                        casa_palleRecuperate = casa_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "T2+":
                        casa_t2_r = casa_t2_r + 1
                    elif partita['eventi'][i]['evento'] == "T2-":
                        casa_t2_s = casa_t2_s + 1
                    elif partita['eventi'][i]['evento'] == "T3+":
                        casa_t3_r = casa_t3_r + 1
                    elif partita['eventi'][i]['evento'] == "T3-":
                        casa_t3_s = casa_t3_s + 1
                    elif partita['eventi'][i]['evento'] == "T1+":
                        casa_t1_r = casa_t1_r + 1
                    elif partita['eventi'][i]['evento'] == "T1-":
                        casa_t1_s = casa_t1_s + 1
                    elif partita['eventi'][i]['evento'] == "PR":
                        casa_palleRecuperate = casa_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "PR":
                        casa_palleRecuperate = casa_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "RD":
                        casa_rimbalzi = casa_rimbalzi + 1
                    elif partita['eventi'][i]['evento'] == "RO":
                        casa_rimbalzi = casa_rimbalzi + 1
                i = i+1
            n_partite = n_partite+1
    if partita['squadra_ospite'] == squadra and len(partita['eventi']) > 0:
        print(partita['eventi'][0]['evento'])
        ospiti_puntiFatti = ospiti_puntiFatti + int(partita['risultato_finale_host'])
        ospiti_puntiSubiti = ospiti_puntiSubiti + int(partita['risultato_finale_guest'])
        i = 0
        while i < len(partita.eventi):
            if partita.eventi[i].giocatore:
                if partita['eventi'][i]['evento'] == "FF":
                    ospiti_falliFatti = ospiti_falliFatti + 1
                elif partita['eventi'][i]['evento'] == "FS":
                    ospiti_falliSubiti = ospiti_falliSubiti + 1
                elif partita['eventi'][i]['evento'] == "PP":
                    ospiti_pallePerse = ospiti_pallePerse + 1
                elif partita['eventi'][i]['evento'] == "PR":
                    ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "T2+":
                    ospiti_t2_r = ospiti_t2_r + 1
                elif partita['eventi'][i]['evento'] == "T2-":
                    ospiti_t2_s = ospiti_t2_s + 1
                elif partita['eventi'][i]['evento'] == "T3+":
                    ospiti_t3_r = ospiti_t3_r + 1
                elif partita['eventi'][i]['evento'] == "T3-":
                    ospiti_t3_s = ospiti_t3_s + 1
                elif partita['eventi'][i]['evento'] == "T1+":
                    ospiti_t1_r = ospiti_t1_r + 1
                elif partita['eventi'][i]['evento'] == "T1-":
                    ospiti_t1_s = ospiti_t1_s + 1
                elif partita['eventi'][i]['evento'] == "PR":
                    ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "PR":
                    ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "RD":
                    ospiti_rimbalzi = ospiti_rimbalzi + 1
                elif partita['eventi'][i]['evento'] == "RO":
                    ospiti_rimbalzi = ospiti_rimbalzi + 1
            i = i+1
        n_partite = n_partite+1