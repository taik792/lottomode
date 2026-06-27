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

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    # CORREZIONE: Cerca la data reale se presente nell'archivio, altrimenti usa la data di oggi
    data_reale = datetime.now().strftime("%d/%m/%Y")
    if "info_concorso" in archivio and "data" in archivio["info_concorso"]:
        data_reale = archivio["info_concorso"]["data"]
    elif "data" in archivio:
        data_reale = archivio["data"]

    risultati_finali = {
        "info_concorso": {"numero": "Algoritmo Isotopo V8", "data": data_reale},
        "previsioni": {}
    }

    archivio_pulito = {k.upper(): v for k, v in archivio.items() if isinstance(v, list)}

    if "BARI" in archivio_pulito and len(archivio_pulito["BARI"]) > 0:
        ultima_estrazione_bari = archivio_pulito["BARI"][-1]
        if isinstance(ultima_estrazione_bari, list) and len(ultima_estrazione_bari) >= 1:
            try:
                primo_bari = int(ultima_estrazione_bari[0])
                ambata = fuori_90(primo_bari + 15)
                abbinamento = calcola_diametrale(ambata)
                
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
    elabora_motore_sommativo()
