import json
import os
from collections import Counter

def calcola_vertibile(numero):
    """Calcola il numero vertibile secondo le regole ufficiali del Lotto."""
    try:
        n = int(numero)
        if n <= 0 or n > 90:
            return 1
        
        # Regola per i Gemelli (11, 22, 33...) -> prendono il diametrale in decina (+/- 5 nella decina)
        if n in [11, 22, 33, 44, 55, 66, 77, 88]:
            if n % 10 <= 5:
                return n + 8
            else:
                return n - 8
        
        # Regola per il numero 90 -> il suo vertibile è 9
        if n == 90:
            return 9
        if n == 9:
            return 90
            
        # Regola per gli Zerbotti (10, 20, 30...) -> es: 10 diventa 1
        if n % 10 == 0:
            return n // 10
            
        # Regola per i numeri a cifra singola (1, 2, 3...) -> es: 3 diventa 30
        if n < 10:
            return n * 10
            
        # Regola standard per numeri a due cifre: si invertono le cifre (es: 16 -> 61)
        decine = n // 10
        unita = n % 10
        vertibile = (unita * 10) + decine
        return vertibile
    except (ValueError, TypeError):
        return 1

def trova_ambata_spia(lista_estrazioni, numero_spia, profondita_ricerca=10):
    """
    Cerca nella storia quante volte è uscito il numero_spia come PRIMO ESTRATTO.
    Raccoglie tutti i numeri usciti nelle estrazioni immediatamente successive
    e restituisce il più frequente (l'Ambata Spia).
    """
    numeri_successivi = []
    
    # Scorriamo l'archivio fino alla penultima estrazione
    for i in range(len(lista_estrazioni) - 1):
        estrazione_corrente = lista_estrazioni[i]
        
        if len(estrazione_corrente) >= 1 and int(estrazione_corrente[0]) == int(numero_spia):
            # Trovata la spia al 1° posto! Prendiamo i numeri dei concorsi successivi (fino a profondita_ricerca)
            fine_finestra = min(i + 1 + profondita_ricerca, len(lista_estrazioni))
            for j in range(i + 1, fine_finestra):
                for num in lista_estrazioni[j]:
                    numeri_successivi.append(int(num))
                    
    if numeri_successivi:
        # Conta il numero più frequente uscito dopo la spia
        conteggio = Counter(numeri_successivi)
        # Escludiamo il numero spia stesso per evitare ripetizioni banali
        if int(numero_spia) in conteggio:
            del conteggio[int(numero_spia)]
        
        if conteggio:
            return conteggio.most_common(1)[0][0]
            
    # Se non c'è abbastanza storico o riscontri, usa una formula di ripiego (es. spia + 1)
    while numero_spia > 90:
        numero_spia -= 90
    return numero_spia if numero_spia > 0 else 1

def elabora_motore():
    if not os.path.exists('estrazioni.json'):
        print("Errore: Il file 'estrazioni.json' non esiste.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    risultati_finali = {
        "info_concorso": {
            "numero": "Metodo Statistico",
            "data": "Spia + Vertibili"
        },
        "previsioni": {}
    }

    if not archivio or not isinstance(archivio, dict):
        print("Errore: Archivio vuoto o formato non valido.")
        return

    for ruota, lista_estrazioni in archivio.items():
        if isinstance(lista_estrazioni, list) and len(lista_estrazioni) > 0:
            # L'ultima estrazione reale in archivio
            ultima_estrazione = lista_estrazioni[-1]
            
            if isinstance(ultima_estrazione, list) and len(ultima_estrazione) >= 1:
                try:
                    # La spia è il PRIMO ESTRATTO dell'ultima estrazione
                    numero_spia = int(ultima_estrazione[0])
                    
                    # 1. Calcolo dell'Ambata tramite lo storico della spia
                    ambata = trova_ambata_spia(lista_estrazioni, numero_spia, profondita_ricerca=12)
                    
                    # 2. Calcolo dell'Abbinamento Ambo tramite il Vertibile dell'Ambata
                    abbinamento = calcola_vertibile(ambata)
                    
                    # Se coincidono (casi rari di protezione), aggiungiamo +1 fuori 90
                    if abbinamento == ambata:
                        abbinamento = ambata + 1 if ambata < 90 else 1

                    risultati_finali["previsioni"][ruota] = {
                        "numeri_estrazione": [int(n) for n in ultima_estrazione[:5]],
                        "spia": numero_spia,
                        "ambata": ambata,
                        "ambo": [ambata, abbinamento]
                    }
                except (ValueError, TypeError) as e:
                    print(f"Salto la ruota {ruota}: {e}")
                    continue

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    
    print("Elaborazione completata! Creato archivio statistico Spie e Vertibili.")

if __name__ == "__main__":
    elabora_motore()
