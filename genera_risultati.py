import json
import os

def fuori_90(numero):
    """Applica la regola del fuori 90 per il gioco del lotto."""
    try:
        n = int(numero)
        while n > 90:
            n -= 90
        while n <= 0:
            n += 90
        return n
    except (ValueError, TypeError):
        return 90

def calcola_diametrale_decina(numero):
    """Calcola il diametrale in decina."""
    if numero % 10 <= 5 and numero % 10 != 0:
        return fuori_90(numero + 5)
    else:
        return fuori_90(numero - 5)

def elabora_motore():
    if not os.path.exists('estrazioni.json'):
        print("Errore: Il file 'estrazioni.json' non esiste.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    # Inizializziamo sempre la struttura corretta per evitare errori in index.html
    risultati_finali = {
        "info_concorso": {
            "numero": "Ultimo",
            "data": "Recente"
        },
        "previsioni": {}
    }

    if not archivio or not isinstance(archivio, dict):
        print("Errore: Archivio vuoto o formato non valido.")
        return

    # Cicla su tutte le ruote presenti nel file (es. Bari, Cagliari ecc.)
    for ruota, lista_estrazioni in archivio.items():
        if isinstance(lista_estrazioni, list) and len(lista_estrazioni) > 0:
            # Prende l'ultima estrazione presente (la più recente in fondo)
            numeri_grezzi = lista_estrazioni[-1]
            
            if isinstance(numeri_grezzi, list) and len(numeri_grezzi) >= 5:
                try:
                    # Forza la conversione in numeri interi per sicurezza
                    numeri = [int(n) for n in numeri_grezzi[:5]]
                    
                    # Calcolo Ambata: Somma del 1° e del 5° estratto
                    primo = numeri[0]
                    quinto = numeri[4]
                    ambata = fuori_90(primo + quinto)
                    
                    # Calcolo Ambo: Ambata + il suo diametrale in decina
                    abbinamento = calcola_diametrale_decina(ambata)
                    
                    if abbinamento == ambata:
                        abbinamento = fuori_90(ambata + 1)

                    # Salva usando il nome esatto della ruota (mantenendo la maiuscola)
                    risultati_finali["previsioni"][ruota] = {
                        "numeri_estrazione": numeri,
                        "ambata": ambata,
                        "ambo": [ambata, abbinamento]
                    }
                except (ValueError, TypeError) as e:
                    print(f"Salto la ruota {ruota} a causa di dati non numerici: {e}")
                    continue

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    
    print("Elaborazione completata! File 'risultati_v4.json' salvato correttamente.")

if __name__ == "__main__":
    elabora_motore()
