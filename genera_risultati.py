import json
import os

def fuori_90(numero):
    while numero > 90: numero -= 90
    while numero <= 0: numero += 90
    return numero

def elabora_motore_geometrico():
    if not os.path.exists('estrazioni.json'): return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    risultati_finali = {
        "info_concorso": {"numero": "Ciclometria Spaziale V7", "data": "Armonie di Chiusura"},
        "previsioni": {}
    }

    nomi_ruote = list(archivio.keys())
    
    # Inizializza tutte le ruote con una previsione di base per evitare schermate vuote
    for r in nomi_ruote:
        if archivio[r]:
            ultimi = [int(n) for n in archivio[r][-1][:5]]
            # Calcolo geometrico standard di sicurezza (Distanza 45 sul primo estratto)
            ambata = fuori_90(ultimi[0] + 45)
            abbinamento = fuori_90(91 - ultimi[0])
            risultati_finali["previsioni"][r] = {
                "numeri_estrazione": ultimi,
                "tipo_calcolo": "Chiusura Diagonale",
                "ambata": ambata,
                "ambo": [ambata, abbinamento],
                "ambetti": [[ambata, fuori_90(abbinamento + 1)], [ambata, fuori_90(abbinamento - 1)]]
            }

    # Cerca armonie reali a passo incrociato tra le ruote (estratti nella stessa posizione)
    for i in range(len(nomi_ruote)):
        for j in range(i + 1, len(nomi_ruote)):
            ruota_a = nomi_ruote[i]
            ruota_b = nomi_ruote[j]
            
            if not archivio[ruota_a] or not archivio[ruota_b]: continue
            
            est_a = [int(n) for n in archivio[ruota_a][-1][:5]]
            est_b = [int(n) for n in archivio[ruota_b][-1][:5]]
            
            # Confronta i numeri nella stessa posizione estrattiva
            for pos in range(min(len(est_a), len(est_b))):
                num_a = est_a[pos]
                num_b = est_b[pos]
                distanza = abs(num_a - num_b)
                
                # Se trova una distanza ciclometrica pura (30 o 45), la struttura è perfetta
                if distanza == 45 or distanza == 30:
                    # Calcola il numero di chiusura geometrica del quadrato
                    ambata_geometrica = fuori_90(num_a + distanza)
                    abbinamento_geometrico = fuori_90(num_b + 1)
                    
                    # Applica la previsione geometrica speciale a entrambe le ruote coinvolte
                    for r_target in [ruota_a, ruota_b]:
                        risultati_finali["previsioni"][r_target] = {
                            "numeri_estrazione": [int(n) for n in archivio[r_target][-1][:5]],
                            "tipo_calcolo": f"Asse {ruota_a}-{ruota_b} (Pos.{pos+1})",
                            "ambata": ambata_geometrica,
                            "ambo": [ambata_geometrica, abbinamento_geometrico],
                            "ambetti": [
                                [ambata_geometrica, fuori_90(abbinamento_geometrico + 1)],
                                [ambata_geometrica, fuori_90(abbinamento_geometrico - 1)]
                            ]
                        }

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    elabora_motore_geometrico()
