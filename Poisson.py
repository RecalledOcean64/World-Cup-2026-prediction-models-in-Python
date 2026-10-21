import math
import os

PROSJEK_GOLOVA_PO_TIMU = 1.3 

def ucitaj_timove_iz_datoteke(ime_datoteke="timovi.txt"):
    """Učitava timove i njihove snage iz tekstualne datoteke."""
    baza_timova = {}
    if not os.path.exists(ime_datoteke):
        print(f"[!] Greška: Datoteka {ime_datoteke} ne postoji u ovom folderu!")
        return baza_timova
        
    with open(ime_datoteke, "r", encoding="utf-8") as f:
        for linija in f:
            linija = linija.strip()
            if not linija or linija.startswith("#"):
                continue
            try:
                ime, napad, obrana = linija.split(",")
                baza_timova[ime.strip()] = {
                    "napad": float(napad.strip()),
                    "obrana": float(obrana.strip())
                }
            except ValueError:
                print(f"[-] Preskočena neispravna linija: {linija}")
    return baza_timova

def izracunaj_vjerojatnost_poisson(lam, k):
    return ((lam ** k) * math.exp(-lam)) / math.factorial(k)

def analiziraj_utakmicu(tim_domacin, tim_gost, timovi_statistika):
    if tim_domacin not in timovi_statistika or tim_gost not in timovi_statistika:
        print("\n[!] Greška: Jedan ili oba tima nisu u bazi podataka.")
        print("Provjerite jeste li točno napisali ime tima u timovi.txt datoteci.")
        return

    lambda_domacin = timovi_statistika[tim_domacin]["napad"] * timovi_statistika[tim_gost]["obrana"] * PROSJEK_GOLOVA_PO_TIMU
    lambda_gost = timovi_statistika[tim_gost]["napad"] * timovi_statistika[tim_domacin]["obrana"] * PROSJEK_GOLOVA_PO_TIMU

    print(f"\n" + "="*50)
    print(f" MEČ: {tim_domacin.upper()} vs {tim_gost.upper()}")
    print(f" Očekivani golovi (xG): {tim_domacin} {lambda_domacin:.2f} - {lambda_gost:.2f} {tim_gost}")
    print("="*50)

    maksimalno_golova = 5
    vjerojatnosti_domacin = [izracunaj_vjerojatnost_poisson(lambda_domacin, i) for i in range(maksimalno_golova + 1)]
    vjerojatnosti_gost = [izracunaj_vjerojatnost_poisson(lambda_gost, i) for i in range(maksimalno_golova + 1)]

    # 1. TABLICA POJEDINAČNIH GOLOVA
    print("\n[ VJEROJATNOST POJEDINAČNIH GOLOVA ]")
    print(f"{'Golovi':<8} | {tim_domacin:<14} | {tim_gost:<14}")
    print("-" * 45)
    for i in range(maksimalno_golova + 1):
        print(f"  {i}      | {vjerojatnosti_domacin[i]*100:>6.2f}%        | {vjerojatnosti_gost[i]*100:>6.2f}%")

    # 2. MATRICA REZULTATA
    print("\n[ MATRICA TOČNIH REZULTATA u % ]")
    zaglavlje = f"{'Dom \\ Gost':<10}|" + "".join([f"{i:>7}" for i in range(maksimalno_golova + 1)])
    print(zaglavlje)
    print("-" * len(zaglavlje))

    pobjeda_domacin = 0
    pobjeda_gost = 0
    nerijeseno = 0

    for g_domacin in range(maksimalno_golova + 1):
        red_ispis = f"    {g_domacin:<6}|"
        for g_gost in range(maksimalno_golova + 1):
            vjerojatnost_rezultata = vjerojatnosti_domacin[g_domacin] * vjerojatnosti_gost[g_gost]
            red_ispis += f"{vjerojatnost_rezultata*100:>7.2f}"
            
            if g_domacin > g_gost:
                pobjeda_domacin += vjerojatnost_rezultata
            elif g_gost > g_domacin:
                pobjeda_gost += vjerojatnost_rezultata
            else:
                nerijeseno += vjerojatnost_rezultata
        print(red_ispis)

    # 3. KONAČNI ISHOD
    print("\n[ PROGNOZA ISHODA UTAKMICE ]")
    print(f" Pobjeda {tim_domacin}: {pobjeda_domacin*100:.2f}%")
    print(f" Neriješeno:       {nerijeseno*100:.2f}%")
    print(f" Pobjeda {tim_gost}: {pobjeda_gost*100:.2f}%")
    print("="*50 + "\n")

# --- GLAVNI PROGRAM ---
timovi_statistika = ucitaj_timove_iz_datoteke()

if timovi_statistika:
    print("--- DOSTUPNE REPREZENTACIJE U BAZI (UČITANE IZ TXT) ---")
    sve_ekipe = list(timovi_statistika.keys())
    for i in range(0, len(sve_ekipe), 4):
        print(", ".join(sve_ekipe[i:i+4]))
    print("-" * 50)

    unos_domacin = input("Unesite domaćina: ").strip()
    unos_gost = input("Unesite gosta: ").strip()

    analiziraj_utakmicu(unos_domacin, unos_gost, timovi_statistika)