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

    data_reale = "26/06/2026"
    
    risultati_finali = {
        "info_concorso": {"numero": "Algoritmo Isotopo V8", "data": data_reale},
        "previsioni": {}
    }

    # Creiamo un archivio con le chiavi tutte in maiuscolo per evitare errori di scrittura
    archivio_pulito = {k.upper(): v for k, v in archivio.items() if isinstance(v, list)}

    # Cerchiamo la ruota di Bari in modo sicuro
    if "BARI" in archivio_pulito and len(archivio_pulito["BARI"]) > 0:
        ultima_estrazione_bari = archivio_pulito["BARI"][-1]
        if isinstance(ultima_estrazione_bari, list) and len(ultima_estrazione_bari) >= 1:
            try:
                # Prende l'INDICE 0 (il primo estratto reale)
                primo_bari = int(ultima_estrazione_bari[0])
                
                # CALCOLO MATEMATICO DEL CAPOGIOCO ISOTOPO
                ambata = fuori_90(primo_bari + 15)
                abbinamento = calcola_diametrale(ambata)
                
                # Generiamo la previsione per Bari e Milano (o le ruote corrispondenti nell'archivio)
                for ruota_chiave, lista_estrazioni in archivio.items():
                    if ruota_chiave.upper() in ["BARI", "MILANO"] and len(lista_estrazioni) > 0:
                        risultati_finali["previsioni"][ruota_chiave] = {
                            "numeri_estrazione": [int(n) for n in lista_estrazioni[-1][:5]],
                            "tipo_calcolo": f"Sommativo da 1° Bari ({primo_bari})",
                            "ambata": ambata,
                            "ambo": [ambata, abbinamento],
                            "ambetti": [
                                [ambata, fuori_90(abbinamento + 1)],
                                [ambata, fuori_90(abbinamento - 1)]
                            ]
                        }
            except (ValueError, IndexError):
                pass

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    elabora_motore_geometrico = elabora_motore_sommativo
    elabora_motore_geometrico()
