import json
import os
from collections import Counter

def calcola_vertibile(numero):
    """Calcola il numero vertibile secondo le regole ufficiali del Lotto."""
    try:
        n = int(numero)
        if n <= 0 or n > 90: return 1
        if n in [11, 22, 33, 44, 55, 66, 77, 88]:
            return n + 8 if n % 10 <= 5 else n - 8
        if n == 90: return 9
        if n == 9: return 90
        if n % 10 == 0: return n // 10
        if n < 10: return n * 10
        return (n % 10 * 10) + (n // 10)
    except (ValueError, TypeError):
        return 1

def analizza_storico_spia(lista_estrazioni, numero_spia, profondita_ricerca=12):
    """
    Trova la spia, calcola l'ambata più frequente, conta i casi totali 
    e quante volte l'ambata è uscita nei cicli successivi (esiti positivi).
    """
    casi_totali = 0
    esiti_positivi = 0
    numeri_successivi = []
    indici_spia = []
    
    # 1. Trova le posizioni della spia nel passato (escludendo l'ultima estrazione)
    for i in range(len(lista_estrazioni) - 1):
        estrazione_corrente = lista_estrazioni[i]
        if len(estrazione_corrente) >= 1 and int(estrazione_corrente[0]) == int(numero_spia):
            indici_spia.append(i)
            casi_totali += 1
            
            # Raccoglie i numeri per determinare l'ambata più frequente
            fine_finestra = min(i + 1 + profondita_ricerca, len(lista_estrazioni))
            for j in range(i + 1, fine_finestra):
                for num in lista_estrazioni[j]:
                    numeri_successivi.append(int(num))
                    
    if not numeri_successivi:
        # Fallback se non ci sono casi passati
        return numero_spia, 0, 0, 0.0

    conteggio = Counter(numeri_successivi)
    if int(numero_spia) in conteggio:
        del conteggio[int(numero_spia)]
        
    if not conteggio:
        return numero_spia, 0, 0, 0.0
        
    # L'ambata statistica è il numero più frequente uscito nei cicli passati
    ambata = conteggio.most_common(1)[0][0]
    
    # 2. Conta in quanti di quei casi l'ambata è uscita davvero nei colpi successivi
    for idx in indici_spia:
        fine_finestra = min(idx + 1 + profondita_ricerca, len(lista_estrazioni))
        uscito_nel_ciclo = False
        for j in range(idx + 1, fine_finestra):
            if int(ambata) in [int(x) for x in lista_estrazioni[j]]:
                uscito_nel_ciclo = True
                break
        if uscito_nel_ciclo:
            esiti_positivi += 1
            
    percentuale_successo = (esiti_positivi / casi_totali * 100) if casi_totali > 0 else 0.0
    return ambata, casi_totali, esiti_positivi, round(percentuale_successo, 1)

def elabora_motore():
    if not os.path.exists('estrazioni.json'):
        print("Errore: Il file 'estrazioni.json' non esiste.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    risultati_finali = {
        "info_concorso": {"numero": "Statistica Avanzata", "data": "Frequenze Spia"},
        "previsioni": {}
    }

    if not archivio or not isinstance(archivio, dict):
        return

    # Fase 1: Calcola i dati per tutte le ruote
    max_percentuale = -1.0
    
    for ruota, lista_estrazioni in archivio.items():
        if isinstance(lista_estrazioni, list) and len(lista_estrazioni) > 0:
            ultima_estrazione = lista_estrazioni[-1]
            if isinstance(ultima_estrazione, list) and len(ultima_estrazione) >= 1:
                try:
                    numero_spia = int(ultima_estrazione[0])
                    
                    # Analisi statistica profonda
                    ambata, casi, positivi, perc = analizza_storico_spia(lista_estrazioni, numero_spia)
                    abbinamento = calcola_vertibile(ambata)
                    
                    if abbinamento == ambata:
                        abbinamento = ambata + 1 if ambata < 90 else 1

                    risultati_finali["previsioni"][ruota] = {
                        "numeri_estrazione": [int(n) for n in ultima_estrazione[:5]],
                        "spia": numero_spia,
                        "ambata": ambata,
                        "ambo": [ambata, abbinamento],
                        "casi_storici": casi,
                        "esiti_positivi": positivi,
                        "percentuale": perc,
                        "consigliata": False # Verrà impostato dopo
                    }
                    
                    if casi >= 2 and perc > max_percentuale:
                        max_percentuale = perc
                        
                except (ValueError, TypeError) as e:
                    continue

    # Fase 2: Identifica e marca la ruota migliore in assoluto (Top Convergenza)
    for ruota, info in risultati_finali["previsioni"].items():
        if info["percentuale"] == max_percentuale and max_percentuale > 0:
            info["consigliata"] = True

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    
    print("Elaborazione completata con individuazione della Ruota Top!")

if __name__ == "__main__":
    elabora_motore()
