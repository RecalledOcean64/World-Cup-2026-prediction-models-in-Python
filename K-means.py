import os
import sys
import subprocess
import pandas as pd

# 1. Osiguravanje potrebnih biblioteka
try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
except ImportError:
    print("[*] Instalacija potrebnih biblioteka (scikit-learn)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

def pokreni_analizu_sudaca(ime_datoteke="suci.txt"):
    if not os.path.exists(ime_datoteke):
        print(f"[!] Greška: Datoteka {ime_datoteke} ne postoji!")
        return

    # Učitavanje podataka
    stupci = ["Ime", "Zuti_Kartoni", "Crveni_Kartoni", "Prekrsaji", "Nadoknada"]
    df = pd.read_csv(ime_datoteke, names=stupci, header=None)
    
    print("=" * 70)
    print("                NAPREDNA K-MEANS ANALIZA SUDACA")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # PRVI ALGORITAM: Grupiranje prema broju kartona (Žuti + Crveni)
    # -------------------------------------------------------------------------
    print("\n\n>>> 1. ALGORITAM: GRUPIRANJE PREMA STROGOĆI (KARTONIMA)")
    print("-" * 70)
    
    X_kartoni = df[["Zuti_Kartoni", "Crveni_Kartoni"]]
    scaler_k = StandardScaler()
    X_k_skalirano = scaler_k.fit_transform(X_kartoni)
    
    kmeans_k = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Klaster_Kartoni"] = kmeans_k.fit_predict(X_k_skalirano)
    
    # Izračun prosjeka po grupama radi automatskog imenovanja
    centri_k = scaler_k.inverse_transform(kmeans_k.cluster_centers_)
    
    # Sortiramo indekse klastera prema prosjeku žutih kartona kako bismo ih točno imenovali
    # Primjer: klaster s najmanje žutih je "Blagi", s najviše je "Strogi"
    poredak_kartona = centri_k[:, 0].argsort()
    imenik_kartona = {
        poredak_kartona[0]: "BLAGI SUCI (Rijetko pokazuju kartone, puštaju slobodniju igru)",
        poredak_kartona[1]: "UMJERENI SUCI (Zlatna sredina, drže utakmicu pod kontrolom standardnim kriterijem)",
        poredak_kartona[2]: "STROGI SUCI (Laki na kartonima, vrlo nizak prag tolerancije za prekršaje)"
    }
    
    # Ispis profila za kartone
    for stari_idx, ime_grupe in imenik_kartona.items():
        print(f"\n[+] PROFIL GRUPE: {ime_grupe}")
        print(f"    - Prosjek žutih: {centri_k[stari_idx, 0]:.2f} po utakmici")
        print(f"    - Prosjek crvenih: {centri_k[stari_idx, 1]:.2f} po utakmici")
        
        # Ispis sudaca koji pripadaju toj grupi
        suci_u_grupi = df[df["Klaster_Kartoni"] == stari_idx]["Ime"].tolist()
        print("    Popis sudaca:")
        for s in suci_u_grupi:
            print(f"      • {s}")

    # -------------------------------------------------------------------------
    # DRUGI ALGORITAM: Grupiranje prema intervalu sudačke nadoknade
    # -------------------------------------------------------------------------
    print("\n\n>>> 2. ALGORITAM: GRUPIRANJE PREMA MINUTAMA NADOKNADE")
    print("-" * 70)
    
    X_nadoknada = df[["Nadoknada"]]
    scaler_n = StandardScaler()
    X_n_skalirano = scaler_n.fit_transform(X_nadoknada)
    
    kmeans_n = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Klaster_Nadoknada"] = kmeans_n.fit_predict(X_n_skalirano)
    
    centri_n = scaler_n.inverse_transform(kmeans_n.cluster_centers_)
    
    # Sortiramo indekse klastera prema prosjeku nadoknade
    poredak_nadoknade = centri_n[:, 0].argsort()
    imenik_nadoknade = {
        poredak_nadoknade[0]: "KRATKA NADOKNADA (Suci koji teže striktnom vremenu, nadoknađuju samo čiste prekide)",
        poredak_nadoknade[1]: "STANDARDNA NADOKNADA (Uobičajen interval nadoknade, između 5.5 i 6.5 minuta)",
        poredak_nadoknade[2]: "DUGA NADOKNADA (Katar-stil suci, nadoknađuju svako slavlje golova i izmjene do u sekundu)"
    }
    
    # Ispis profila za nadoknadu
    for stari_idx, ime_grupe in imenik_nadoknade.items():
        print(f"\n[+] PROFIL GRUPE: {ime_grupe}")
        print(f"    - Prosječna dužina nadoknade: {centri_n[stari_idx, 0]:.1f} minuta")
        
        # Ispis sudaca koji pripadaju toj grupi
        suci_u_grupi = df[df["Klaster_Nadoknada"] == stari_idx]["Ime"].tolist()
        print("    Popis sudaca:")
        for s in suci_u_grupi:
            print(f"      • {s}")
            
    print("\n" + "=" * 70)

# Pokretanje skripte
pokreni_analizu_sudaca()