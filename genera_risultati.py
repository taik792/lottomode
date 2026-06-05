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

def calcola_diametrale_45(numero):
    """Calcola il diametrale naturale (Distanza 45 perfetta sul cerchio ciclometrico)."""
    if numero <= 45:
        return numero + 45
    else:
        return numero - 45

def elabora_motore():
    if not os.path.exists('estrazioni.json'):
        print("Errore: Il file 'estrazioni.json' non esiste.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

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

    for ruota, lista_estrazioni in archivio.items():
        if isinstance(lista_estrazioni, list) and len(lista_estrazioni) > 0:
            numeri_grezzi = lista_estrazioni[-1]
            
            if isinstance(numeri_grezzi, list) and len(numeri_grezzi) >= 5:
                try:
                    numeri = [int(n) for n in numeri_grezzi[:5]]
                    
                    # Calcolo Ambata: Somma del 1° e del 5° estratto
                    primo = numeri[0]
                    quinto = numeri[4]
                    ambata = fuori_90(primo + quinto)
                    
                    # NUOVO CALCOLO AMBO: Distanza 45 (Consigliata)
                    abbinamento = calcola_diametrale_45(ambata)
                    
                    # Protezione se per assurdo i numeri coincidessero
                    if abbinamento == ambata:
                        abbinamento = fuori_90(ambata + 1)

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
    
    print("Elaborazione completata con successo con Distanza 45! File 'risultati_v4.json' salvato.")

if __name__ == "__main__":
    elabora_motore()
