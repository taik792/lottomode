import json
import os
from datetime import datetime

def fuori_90(numero):
    while numero > 90: numero -= 90
    while numero <= 0: numero += 90
    return numero

def calcola_diametrale(numero):
    if numero <= 45: return numero + 45
    return numero - 45

def elabora_motore_sommativo():
    if not os.path.exists('estrazioni.json'): return

    FISSO_OTTIMIZZATO = 25 

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    # Identifica la data reale
    data_reale = datetime.now().strftime("%d/%m/%Y")
    if "info_concorso" in archivio and "data" in archivio["info_concorso"]:
        data_reale = archivio["info_concorso"]["data"]
    elif "data" in archivio:
        data_reale = archivio["data"]

    # Carica o inizializza lo storico persistente delle previsioni generata
    storico_previsioni = []
    if os.path.exists('storico_cronologico_v8.json'):
        with open('storico_cronologico_v8.json', 'r', encoding='utf-8') as sf:
            try: storico_previsioni = json.load(sf)
            except: storico_previsioni = []

    risultati_finali = {
        "info_concorso": {"numero": "Lotto Intelligence V8", "data": data_reale},
        "previsioni": {},
        "storico_verificato": []
    }

    archivio_pulito = {k.upper(): v for k, v in archivio.items() if isinstance(v, list)}

    if "BARI" in archivio_pulito and len(archivio_pulito["BARI"]) > 0:
        # Recuperiamo l'intera sequenza per calcolare le posizioni
        lista_bari = archivio_pulito["BARI"]
        lista_milano = archivio_pulito.get("MILANO", [])
        
        ultima_estrazione_bari = lista_bari[-1]
        
        if isinstance(ultima_estrazione_bari, list) and len(ultima_estrazione_bari) >= 1:
            try:
                primo_bari = int(ultima_estrazione_bari[0])
                ambata = fuori_90(primo_bari + FISSO_OTTIMIZZATO)
                abbinamento = calcola_diametrale(ambata)
                ambo_secco = [ambata, abbinamento]
                ambetti = [
                    [ambata, fuori_90(abbinamento + 1)],
                    [ambata, fuori_90(abbinamento - 1)]
                ]
                
                # Registra la previsione corrente se non esiste già nello storico salvato su file
                if not any(x['data'] == data_reale for x in storico_previsioni):
                    storico_previsioni.append({
                        "data": data_reale,
                        "primo_bari": primo_bari,
                        "ambata": ambata,
                        "ambo": ambo_secco,
                        "ambetti": ambetti,
                        "indice_archivio": len(lista_bari) - 1
                    })
                    with open('storico_cronologico_v8.json', 'w', encoding='utf-8') as sf:
                        json.dump(storico_previsioni, sf, indent=4, ensure_ascii=False)

                # Costruisce la sezione "Previsione in Corso"
                for ruota_chiave in ["BARI", "MILANO"]:
                    if ruota_chiave in archivio_pulito and len(archivio_pulito[ruota_chiave]) > 0:
                        risultati_finali["previsioni"][ruota_chiave] = {
                            "numeri_estrazione": [int(n) for n in archivio_pulito[ruota_chiave][-1][:5]],
                            "tipo_calcolo": f"Sommativo da 1° Bari ({primo_bari}) +{FISSO_OTTIMIZZATO}",
                            "ambata": ambata,
                            "ambo": ambo_secco,
                            "ambetti": ambetti
                        }

                # Ciclo di verifica per ogni previsione passata salvata nel file
                for prev in storico_previsioni:
                    idx_inizio = prev["indice_archivio"]
                    # Calcola quanti colpi sono passati dall'estrazione di calcolo
                    colpi_passati = (len(lista_bari) - 1) - idx_inizio
                    
                    if colpi_passati == 0:
                        continue # È la previsione corrente appena nata stasera
                        
                    esito = "In gioco"
                    colpo_vincita = None
                    
                    # Scansione dei colpi successivi alla ricerca di vincite reali
                    for c in range(1, colpi_passati + 1):
                        curr_idx = idx_inizio + c
                        if curr_idx >= len(lista_bari): break
                        
                        ba_nums = [int(n) for n in lista_bari[curr_idx][:5]]
                        mi_nums = [int(n) for n in lista_milano[curr_idx][:5]] if curr_idx < len(lista_milano) else []
                        
                        # Controllo Ambo
                        if (prev["ambo"][0] in ba_nums and prev["ambo"][1] in ba_nums) or (prev["ambo"][0] in mi_nums and prev["ambo"][1] in mi_nums):
                            esito = "AMBO SECCO VINCENTE!"
                            colpo_vincita = c
                            break
                        # Controllo Ambata
                        elif (prev["ambata"] in ba_nums) or (prev["ambata"] in mi_nums):
                            if esito == "In gioco":
                                esito = "Ambata Vincente"
                                colpo_vincita = c

                    risultati_finali["storico_verificato"].append({
                        "data": prev["data"],
                        "ambata": prev["ambata"],
                        "ambo": f"{prev['ambo'][0]} - {prev['ambo'][1]}",
                        "colpi": f"{colpi_passati}° Colpo" if esito == "In gioco" else f"VINTO al {colpo_vincita}° colpo",
                        "stato": esito
                    })

            except (ValueError, IndexError):
                pass

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    elabora_motore_sommativo()
