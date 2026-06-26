import json
import os

def fuori_90(numero):
    while numero > 90: numero -= 90
    while numero <= 0: numero += 90
    return numero

def calcola_diametrale(numero):
    if numero <= 45: return numero + 45
    return numero - 45

def elabora_motore_sommativo():
    if not os.path.exists('estrazioni.json'): return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    # Impostiamo la data dell'ultimo concorso reale di stasera
    data_reale = "26/06/2026"
    
    risultati_finali = {
        "info_concorso": {"numero": "Algoritmo Isotopo V8", "data": data_reale},
        "previsioni": {}
    }

    # Estraiamo il primo numero di Bari come Capogioco dell'intera estrazione
    if "BARI" in archivio and len(archivio["BARI"]) > 0:
        ultimo_bari = [int(n) for n in archivio["BARI"][-1][:5]]
        primo_bari = ultimo_bari[0]
        
        # CALCOLO MATEMATICO FISSO
        ambata = fuori_90(primo_bari + 15)
        abbinamento = calcola_diametrale(ambata)
        
        # Applichiamo la previsione unificata solo su BARI e MILANO
        for r_target in ["BARI", "MILANO"]:
            if r_target in archivio and len(archivio[r_target]) > 0:
                risultati_finali["previsioni"][r_target] = {
                    "numeri_estrazione": [int(n) for n in archivio[r_target][-1][:5]],
                    "tipo_calcolo": f"Sommativo da 1° Bari ({primo_bari})",
                    "ambata": ambata,
                    "ambo": [ambata, abbinamento],
                    "ambetti": [
                        [ambata, fuori_90(abbinamento + 1)],
                        [ambata, fuori_90(fuori_90(abbinamento - 1))]
                    ]
                }

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    elabora_motore_sommativo()
