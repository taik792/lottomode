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

    if not archivio or not isinstance(archivio, dict):
        print("Errore: Struttura di 'estrazioni.json' non valida (deve essere un dizionario di ruote).")
        return

    risultati_finali = {
        "info_concorso": {
            "numero": "Ultimo",
            "data": "Recente"
        },
        "previsioni": {}
    }

    # Cicla su ogni ruota presente nel dizionario principale
    for ruota, lista_estrazioni in archivio.items():
        if isinstance(lista_estrazioni, list) and len(lista_estrazioni) > 0:
            # Prende l'ultima estrazione della lista (la più recente in fondo)
            numeri = lista_estrazioni[-1]
            
            if isinstance(numeri, list) and len(numeri) >= 5:
                # Calcolo Ambata: Somma del 1° e del 5° estratto
                primo = numeri[0]
                quinto = numeri[4]
                ambata = fuori_90(primo + quinto)
                
                # Calcolo Ambo: Ambata + il suo diametrale in decina
                abbinamento = calcola_diametrale_decina(ambata)
                
                if abbinamento == ambata:
                    abbinamento = fuori_90(ambata + 1)

                risultati_finali["previsioni"][ruota] = {
                    "numeri_estrazione": numeri,
                    "ambata": ambata,
                    "ambo": [ambata, abbinamento]
                }

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    
    print("Elaborazione completata con successo! File 'risultati_v4.json' aggiornato.")

if __name__ == "__main__":
    elabora_motore()
