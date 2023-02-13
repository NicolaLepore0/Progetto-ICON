import csv
import json

with open("../dataset/squadre.txt", "r") as file:
    lista = [riga.strip() for riga in file]

with open("../dataset/partita.json", "r") as file:
    data = json.load(file)

with open("../dataset/partita21.json", "r") as file1:
    data2 = json.load(file1)

with open("../dataset/squadre.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
    'casa_puntiFatti',
    'casa_puntiSubiti',
    'casa_falliFatti',
    'casa_falliSubiti',
    'casa_pallePerse',
    'casa_palleRecuperate',
    'casa_t2_r',
    'casa_t2_s',
    'casa_t3_r',
    'casa_t3_s',
    'casa_t1_r',
    'casa_t1_s',
    'casa_rimbalzi_o',
    'casa_rimbalzi_d',
    'ospiti_puntiFatti',
    'ospiti_puntiSubiti',
    'ospiti_falliFatti',
    'ospiti_falliSubiti',
    'ospiti_pallePerse',
    'ospiti_palleRecuperate',
    'ospiti_t2_r',
    'ospiti_t2_s',
    'ospiti_t3_r',
    'ospiti_t3_s',
    'ospiti_t1_r',
    'ospiti_t1_s',
    'ospiti_rimbalzi_o',
    'ospiti_rimbalzi_d',
    'result'
    ])
    for partita in data:
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
        casa_rimbalzi_d = 0
        casa_rimbalzi_o = 0
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
        ospiti_rimbalzi_d = 0
        ospiti_rimbalzi_o = 0
        result = ""
        if len(partita['eventi']) > 0:
            casa_puntiFatti = casa_puntiFatti + int(partita['risultato_finale_host'])
            casa_puntiSubiti = casa_puntiSubiti + int(partita['risultato_finale_guest'])
            if casa_puntiFatti > casa_puntiSubiti:
                result = 'victory'
            else:
                result = 'lose'
            i = 0
            while i < len(partita['eventi']):
                    if partita['eventi'][i]['evento'] == "FF" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_falliFatti = casa_falliFatti + 1
                    elif partita['eventi'][i]['evento'] == "FS" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_falliSubiti = casa_falliSubiti + 1
                    elif partita['eventi'][i]['evento'] == "PP" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_pallePerse = casa_pallePerse + 1
                    elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_palleRecuperate = casa_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "T2+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_t2_r = casa_t2_r + 1
                    elif partita['eventi'][i]['evento'] == "T2-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_t2_s = casa_t2_s + 1
                    elif partita['eventi'][i]['evento'] == "T3+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_t3_r = casa_t3_r + 1
                    elif partita['eventi'][i]['evento'] == "T3-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_t3_s = casa_t3_s + 1
                    elif partita['eventi'][i]['evento'] == "T1+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_t1_r = casa_t1_r + 1
                    elif partita['eventi'][i]['evento'] == "T1-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_t1_s = casa_t1_s + 1
                    elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_palleRecuperate = casa_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_palleRecuperate = casa_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "RD" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_rimbalzi_d = casa_rimbalzi_d + 1
                    elif partita['eventi'][i]['evento'] == "RO" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                        casa_rimbalzi_o = casa_rimbalzi_o + 1
                    i = i+1

        if len(partita['eventi']) > 0:
            ospiti_puntiFatti = ospiti_puntiFatti + int(partita['risultato_finale_guest'])
            ospiti_puntiSubiti = ospiti_puntiSubiti + int(partita['risultato_finale_host'])
            if ospiti_puntiFatti > ospiti_puntiSubiti:
                result = 'victory'
            else:
                result = 'lose'
            i = 0
            while i < len(partita['eventi']):
                    if partita['eventi'][i]['evento'] == "FF" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_falliFatti = ospiti_falliFatti + 1
                    elif partita['eventi'][i]['evento'] == "FS" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_falliSubiti = ospiti_falliSubiti + 1
                    elif partita['eventi'][i]['evento'] == "PP" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_pallePerse = ospiti_pallePerse + 1
                    elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "T2+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_t2_r = ospiti_t2_r + 1
                    elif partita['eventi'][i]['evento'] == "T2-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_t2_s = ospiti_t2_s + 1
                    elif partita['eventi'][i]['evento'] == "T3+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_t3_r = ospiti_t3_r + 1
                    elif partita['eventi'][i]['evento'] == "T3-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_t3_s = ospiti_t3_s + 1
                    elif partita['eventi'][i]['evento'] == "T1+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_t1_r = ospiti_t1_r + 1
                    elif partita['eventi'][i]['evento'] == "T1-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_t1_s = ospiti_t1_s + 1
                    elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                    elif partita['eventi'][i]['evento'] == "RD" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_rimbalzi_d = ospiti_rimbalzi_d + 1
                    elif partita['eventi'][i]['evento'] == "RO" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                        ospiti_rimbalzi_o = ospiti_rimbalzi_o + 1
                    i = i+1
        if casa_puntiFatti > 0:
            writer.writerow([casa_puntiFatti, casa_puntiSubiti,
                          casa_falliFatti,
                          casa_falliSubiti,
                          casa_pallePerse,
                          casa_palleRecuperate,
                          casa_t2_r,
                          casa_t2_s,
                          casa_t3_r,
                          casa_t3_s,
                          casa_t1_r,
                          casa_t1_s,
                          casa_rimbalzi_o,
                          casa_rimbalzi_d,
                          ospiti_puntiFatti,
                          ospiti_puntiSubiti,
                          ospiti_falliFatti,
                          ospiti_falliSubiti,
                          ospiti_pallePerse,
                          ospiti_palleRecuperate,
                          ospiti_t2_r,
                          ospiti_t2_s,
                          ospiti_t3_r,
                          ospiti_t3_s,
                          ospiti_t1_r,
                          ospiti_t1_s,
                          ospiti_rimbalzi_o,
                          ospiti_rimbalzi_d,
                          result])
    for partita in data2:

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
        casa_rimbalzi_o= 0
        casa_rimbalzi_d =0
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
        ospiti_rimbalzi_o = 0
        ospiti_rimbalzi_d = 0
        result = ""
        if len(partita['eventi']) > 0:
            casa_puntiFatti = casa_puntiFatti + int(partita['risultato_finale_host'])
            casa_puntiSubiti = casa_puntiSubiti + int(partita['risultato_finale_guest'])
            if casa_puntiFatti > casa_puntiSubiti:
                result = 'victory'
            else:
                result = 'lose'
            i = 0
            while i < len(partita['eventi']):
                if partita['eventi'][i]['evento'] == "FF" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_falliFatti = casa_falliFatti + 1
                elif partita['eventi'][i]['evento'] == "FS" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_falliSubiti = casa_falliSubiti + 1
                elif partita['eventi'][i]['evento'] == "PP" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_pallePerse = casa_pallePerse + 1
                elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_palleRecuperate = casa_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "T2+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_t2_r = casa_t2_r + 1
                elif partita['eventi'][i]['evento'] == "T2-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_t2_s = casa_t2_s + 1
                elif partita['eventi'][i]['evento'] == "T3+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_t3_r = casa_t3_r + 1
                elif partita['eventi'][i]['evento'] == "T3-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_t3_s = casa_t3_s + 1
                elif partita['eventi'][i]['evento'] == "T1+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_t1_r = casa_t1_r + 1
                elif partita['eventi'][i]['evento'] == "T1-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_t1_s = casa_t1_s + 1
                elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_palleRecuperate = casa_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_palleRecuperate = casa_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "RD" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_rimbalzi_d = casa_rimbalzi_d + 1
                elif partita['eventi'][i]['evento'] == "RO" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_casa']:
                    casa_rimbalzi_o = casa_rimbalzi_o + 1
                i = i+1

        if len(partita['eventi']) > 0:
            ospiti_puntiFatti = ospiti_puntiFatti + int(partita['risultato_finale_guest'])
            ospiti_puntiSubiti = ospiti_puntiSubiti + int(partita['risultato_finale_host'])
            if ospiti_puntiFatti > ospiti_puntiSubiti:
                result = 'victory'
            else:
                result = 'lose'
            i = 0
            while i < len(partita['eventi']):
                if partita['eventi'][i]['evento'] == "FF" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_falliFatti = ospiti_falliFatti + 1
                elif partita['eventi'][i]['evento'] == "FS" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_falliSubiti = ospiti_falliSubiti + 1
                elif partita['eventi'][i]['evento'] == "PP" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_pallePerse = ospiti_pallePerse + 1
                elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "T2+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_t2_r = ospiti_t2_r + 1
                elif partita['eventi'][i]['evento'] == "T2-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_t2_s = ospiti_t2_s + 1
                elif partita['eventi'][i]['evento'] == "T3+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_t3_r = ospiti_t3_r + 1
                elif partita['eventi'][i]['evento'] == "T3-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_t3_s = ospiti_t3_s + 1
                elif partita['eventi'][i]['evento'] == "T1+" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_t1_r = ospiti_t1_r + 1
                elif partita['eventi'][i]['evento'] == "T1-" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_t1_s = ospiti_t1_s + 1
                elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "PR" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_palleRecuperate = ospiti_palleRecuperate + 1
                elif partita['eventi'][i]['evento'] == "RD" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_rimbalzi_d = ospiti_rimbalzi_d + 1
                elif partita['eventi'][i]['evento'] == "RO" and partita['eventi'][i]['giocatore']['squadra'] == partita['squadra_ospite']:
                    ospiti_rimbalzi_o = ospiti_rimbalzi_o + 1
                i = i+1
        if casa_puntiFatti > 0:
            writer.writerow([casa_puntiFatti, casa_puntiSubiti,
                             casa_falliFatti,
                             casa_falliSubiti,
                             casa_pallePerse,
                             casa_palleRecuperate,
                             casa_t2_r,
                             casa_t2_s,
                             casa_t3_r,
                             casa_t3_s,
                             casa_t1_r,
                             casa_t1_s,
                             casa_rimbalzi_o,
                             casa_rimbalzi_d,
                             ospiti_puntiFatti,
                             ospiti_puntiSubiti,
                             ospiti_falliFatti,
                             ospiti_falliSubiti,
                             ospiti_pallePerse,
                             ospiti_palleRecuperate,
                             ospiti_t2_r,
                             ospiti_t2_s,
                             ospiti_t3_r,
                             ospiti_t3_s,
                             ospiti_t1_r,
                             ospiti_t1_s,
                             ospiti_rimbalzi_o,
                             ospiti_rimbalzi_d,
                             result])