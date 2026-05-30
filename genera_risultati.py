import json
import os

ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    if not os.path.exists(ESTRAZIONI_FILE):
        return {}
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcola_distanza_ciclometrica(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def determina_esagono(numero):
    resto = numero % 15
    return 15 if resto == 0 else resto

def analizza_statistiche_ruote(archivio):
    """
    Analizza la cronologia per calcolare ritardi e frequenze recenti (ultimi 18 colpi).
    """
    stats = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()
        if not isinstance(estrazioni_ruota, list) or len(estrazioni_ruota) == 0:
            continue
            
        ritardi = {n: 0 for n in range(1, 91)}
        frequenza_recente = {n: 0 for n in range(1, 91)}
        
        ultime_18 = estrazioni_ruota[-18:] if len(estrazioni_ruota) >= 18 else estrazioni_ruota
        
        for estrazione in ultime_18:
            if isinstance(estrazione, list):
                for num in estrazione[:5]:
                    if 1 <= int(num) <= 90:
                        frequenza_recente[int(num)] += 1
                        
        for n in range(1, 91):
            ritardo = 0
            trovato = False
            for estrazione in reversed(estrazioni_ruota):
                if isinstance(estrazione, list) and n in [int(x) for x in estrazione[:5]]:
                    trovato = True
                    break
                ritardo += 1
            stats_val = ritardo if trovato else len(estrazioni_ruota)
            ritardi[n] = stats_val
            
        stats[nome_standard] = {
            "ritardi": ritardi,
            "frequenze_18": frequenza_recente
        }
    return stats

def calcola_peso_statistico(n, ruota, stats):
    """
    Assegna un punteggio di precisione al numero basato su ritardo ideale e ciclicità.
    """
    if ruota not in stats:
        return 50  
        
    ritardo = stats[ruota]["ritardi"].get(n, 0)
    freq = stats[ruota]["frequenze_18"].get(n, 0)
    
    punteggio = 50
    
    if freq == 1:
        punteggio += 15
    elif freq == 2:
        punteggio += 20
    elif freq == 0:  
        punteggio += 5
    else:            
        punteggio -= 10
        
    if 10 <= ritardo <= 36:
        punteggio += 25
    elif 1 <= ritardo <= 9: 
        punteggio -= 15
    elif ritardo > 54:      
        punteggio -= 10
        
    return punteggio

def esegui_elaborazione_motore():
    print("=== AVVIO MOTORE GEOMETRICO-STATISTICO v7.3 ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    statistiche_ruote = analizza_statistiche_ruote(archivio)

    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()
        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima = estrazioni_ruota[-1]
            if isinstance(ultima, list) and len(ultima) >= 5:
                ruote_pulite[nome_standard] = [int(x) for x in ultima[:5]]

    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    mappa_calore = {r: "rossa" if r in ruote_rosse else "grigia" if r in ruote_grigie else "gialla" for r in ruote_pulite}

    elenco_ruote = sorted(list(ruote_pulite.keys()))
    previsioni_generate = {}

    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            for p in range(5):
                n1 = ruote_pulite[r1][p]
                n2 = ruote_pulite[r2][p]

                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    somma_isotopa = (n1 + n2) % 90 or 90
                    
                    # L'ambata principale rimane il punto di equilibrio geometrico
                    ambata = (somma_isotopa + 45) % 90 or 90
                    
                    # --- NUOVA LOGICA: CHIUSURA DIAGONALE DINAMICA ---
                    # Invece del passo fisso +15 che bloccava i numeri, calcoliamo il passo
                    # basandoci sul simmetrico dinamico rispetto al numero statistico più caldo
                    peso_n1 = calcola_peso_statistico(n1, r1, statistiche_ruote)
                    peso_n2 = calcola_peso_statistico(n2, r2, statistiche_ruote)
                    
                    passo_dinamico = 30 if peso_n1 >= peso_n2 else 60
                    abbinamento = (ambata + passo_dinamico) % 90 or 90

                    if ambata == abbinamento or ambata in [n1, n2] or abbinamento in [n1, n2]:
                        ambata = (n1 + 45) % 90 or 90
                        abbinamento = (n2 + 45) % 90 or 90
                    
                    if ambata == abbinamento:
                        abbinamento = (ambata + 15) % 90 or 90

                    numeri_gioco = sorted([ambata, abbinamento])
                    chiave_ambo = f"{numeri_gioco[0]}-{numeri_gioco[1]}"

                    peso_r1 = calcola_peso_statistico(numeri_gioco[0], r1, statistiche_ruote) + calcola_peso_statistico(numeri_gioco[1], r1, statistiche_ruote)
                    peso_r2 = calcola_peso_statistico(numeri_gioco[0], r2, statistiche_ruote) + calcola_peso_statistico(numeri_gioco[1], r2, statistiche_ruote)
                    media_peso = (peso_r1 + peso_r2) / 4

                    base_score = 140 if dist == 15 else 130 if dist == 30 else 120
                    score_finale_numerico = int(base_score + (media_peso * 0.4))
                    
                    if score_finale_numerico > 195: score_finale_numerico = 195
                    str_score = f"{score_finale_numerico}%"

                    tipo_tabellone = "nuovi" if dist == 15 else "colpo2" if dist == 30 else "colpo3"

                    if chiave_ambo in previsioni_generate:
                        if r1 not in previsioni_generate[chiave_ambo]["ruote"]:
                            previsioni_generate[chiave_ambo]["ruote"] += f", {r1}"
                            vecchio_score = int(previsioni_generate[chiave_ambo]["score"].replace("%", ""))
                            previsioni_generate[chiave_ambo]["score"] = f"{min(vecchio_score + 5, 198)}%"
                    else:
                        previsioni_generate[chiave_ambo] = {
                            "ruote": f"{r1} - {r2}",
                            "numeri": numeri_gioco,
                            "score": str_score,
                            "colore_r1": mappa_calore[r1],
                            "colore_r2": mappa_calore[r2],
                            "tipo": tipo_tabellone,
                            "valore_ordinamento": score_finale_numerico
                        }

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    previsioni_ordinate = sorted(previsioni_generate.values(), key=lambda x: x["valore_ordinamento"], reverse=True)

    for pred in previsioni_ordinate:
        struttura = {
            "ruote": pred["ruote"],
            "numeri": pred["numeri"],
            "score": pred["score"],
            "colore_r1": pred["colore_r1"],
            "colore_r2": pred["colore_r2"]
        }
        if pred["tipo"] == "nuovi":
            tabellone_nuovi.append(struttura)
        elif pred["tipo"] == "colpo2":
            tabellone_colpo2.append(struttura)
        elif pred["tipo"] == "colpo3":
            tabellone_colpo3.append(struttura)

    if not tabellone_nuovi:
        tabellone_nuovi = [{"ruote": "Nessuna Struttura", "numeri": [15, 60], "score": "140%", "colore_r1": "gialla", "colore_r2": "gialla"}]
    if not tabellone_colpo2:
        tabellone_colpo2 = [{"ruote": "Nessuna Struttura", "numeri": [30, 75], "score": "130%", "colore_r1": "gialla", "colore_r2": "gialla"}]
    if not tabellone_colpo3:
        tabellone_colpo3 = [{"ruote": "Nessuna Struttura", "numeri": [45, 90], "score": "120%", "colore_r1": "gialla", "colore_r2": "gialla"}]

    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:6],
            "colpo2": tabellone_colpo2[:6],
            "colpo3": tabellone_colpo3[:6]
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    print("=== MOTORE IBRIDO GEOMETRICO-STATISTICO AGGIORNATO CON SUCCESSO ===")

if __name__ == "__main__":
    esegui_elaborazione_motore()
