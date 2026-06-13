import json
import os

def fuori_90(numero):
    """Applica la regola matematica del fuori 90."""
    while numero > 90: numero -= 90
    while numero <= 0: numero += 90
    return numero

def elabora_motore_sommativo():
    if not os.path.exists('estrazioni.json'): return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    risultati_finali = {
        "info_concorso": {"numero": "Algoritmo Sommativo V6", "data": "Nuova Strategia Matematica"},
        "previsioni": {}
    }

    for ruota, lista_estrazioni in archivio.items():
        if isinstance(lista_estrazioni, list) and len(lista_estrazioni) > 0:
            ultima_estrazione = lista_estrazioni[-1]
            if isinstance(ultima_estrazione, list) and len(ultima_estrazione) >= 1:
                try:
                    # Prendiamo il 1° estratto della ruota (Capogioco Naturale)
                    primo_estratto = int(ultima_estrazione[0])
                    
                    # ALGORITMO: Somma fissa +7 e +21 per trovare la nuova Ambata Principale
                    ambata = fuori_90(primo_estratto + 7)
                    
                    # ABBINAMENTO: Chiusura diametrale in base 91 per l'Ambo Secco
                    abbinamento = fuori_90(91 - ambata)
                    
                    if abbinamento == ambata: 
                        abbinamento = fuori_90(ambata + 45)

                    # Ambetti protettivi basati solo sull'abbinamento principale
                    ambetti = [
                        [ambata, fuori_90(abbinamento + 1)],
                        [ambata, fuori_90(abbinamento - 1)]
                    ]

                    risultati_finali["previsioni"][ruota] = {
                        "numeri_estrazione": [int(n) for n in ultima_estrazione[:5]],
                        "spia": primo_estratto, # Usato come riferimento visivo del 1° estratto
                        "ambata": ambata,
                        "ambo": [ambata, abbinamento],
                        "ambetti": ambetti
                    }
                except (ValueError, TypeError, IndexError):
                    continue

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.load # Correzione scrittura file di output sicuro
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    elabora_motore_sommativo()
