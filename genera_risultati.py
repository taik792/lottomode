import json
import os

def fuori_90(numero):
    """Applica la regola del fuori 90 per il gioco del lotto."""
    while numero > 90:
        numero -= 90
    while numero <= 0:
        numero += 90
    return numero

def calcola_diametrale_decina(numero):
    """Calcola il diametrale in decina (es: se finisce per 1-5 aggiunge 5, altrimenti sottrae 5)."""
    if numero % 10 <= 5 and numero % 10 != 0:
        return fuori_90(numero + 5)
    else:
        return fuori_90(numero - 5)

def elabora_motore():
    # Verifica presenza file archivio
    if not os.path.exists('estrazioni.json'):
        print("Errore: Il file 'estrazioni.json' non esiste.")
        return

    # Carica le estrazioni
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    if not archivio:
        print("Errore: L'archivio delle estrazioni è vuoto.")
        return

    # Prende l'ultima estrazione (la più recente, supponendo sia l'ultima della lista)
    ultima_estrazione = archivio[-1]
    data_estrazione = ultima_estrazione.get("data", "Sconosciuta")
    concorso = ultima_estrazione.get("concorso", "N/D")
    ruote_dati = ultima_estrazione.get("ruote", {})

    risultati_finali = {
        "info_concorso": {
            "numero": concorso,
            "data": data_estrazione
        },
        "previsioni": {}
    }

    # Calcolo Ambata e Ambo per ogni ruota presente
    for ruota, numeri in ruote_dati.items():
        if len(numeri) >= 5:
            # Calcolo Ambata: Somma del 1° e del 5° estratto
            primo = numeri[0]
            quinto = numeri[4]
            ambata = fuori_90(primo + quinto)
            
            # Calcolo Ambo: Ambata + il suo diametrale in decina
            abbinamento = calcola_diametrale_decina(ambata)
            
            # Se l'abbinamento è uguale all'ambata, cambiamo logica temporaneamente (+1)
            if abbinamento == ambata:
                abbinamento = fuori_90(ambata + 1)

            risultati_finali["previsioni"][ruota] = {
                "numeri_estrazione": numeri,
                "ambata": ambata,
                "ambo": [ambata, abbinamento]
            }

    # Salva il risultato nel file risultati_v4.json
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    
    print("Elaborazione completata con successo! File 'risultati_v4.json' aggiornato.")

if __name__ == "__main__":
    elabora_motore()
