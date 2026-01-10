#!/usr/bin/env python3
import platform       # För att kolla vilket operativsystem som körs
import os             # För att hantera filer och mappar i systemet
import hashlib        # För att skapa säkra hash-summor av lösenord
import urllib.request # För att kunna hämta data från internet (API)
import json           # För att tolka JSON-svar från API:er
import logging        # För att logga händelser och fel till fil

def system_koll():
    """
    Kollar att systemet uppfyller kraven innan start.
    1. Kollar skrivrättigheter (för loggfilen).
    2. Kollar internetanslutning (för API:er).
    """
    # Test 1: Skrivrättigheter i nuvarande mapp
    if not os.access(".", os.W_OK):
        print("[-] Fel: Saknar skrivrättigheter i mappen. Kan inte skapa loggfil.")
        return False

    # Test 2: Internetanslutning (försöker nå Google snabbt)
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
    except Exception:
        print("[-] Fel: Ingen internetanslutning. Kan inte nå databaser.")
        return False

    return True

def kolla_mapp(password):
    """
    Söker igenom alla filer i mappen 'ordlistor' efter lösenordet.
    Returnerar True vid matchning, annars False.
    """
    # Hitta var detta script ligger och bygg sökvägen till 'ordlistor' därifrån
    script_mapp = os.path.dirname(os.path.abspath(__file__))
    mappnamn = os.path.join(script_mapp, "ordlistor")
    
    # Kontrollera att mappen finns
    if not os.path.exists(mappnamn):
        print(f"[-] Systemfel: Mappen '{mappnamn}' saknas.")
        logging.error(f"Mappen '{mappnamn}' saknas.")
        return False
    
    try:
        # Loopar igenom alla filer som finns i mappen
        for filnamn in os.listdir(mappnamn):
            sokvag = os.path.join(mappnamn, filnamn)
            
            # Vi öppnar bara riktiga filer
            if os.path.isfile(sokvag):
                with open(sokvag, "r", encoding="utf-8", errors="ignore") as fil:
                    for rad in fil:
                        # Rensar bort radbrytningar och jämför med lösenordet
                        if rad.strip() == password:
                            return True
    except Exception as e:
        print(f"[-] Ett fel uppstod: {e}")
        logging.error(f"Fel vid läsning av fil: {e}")
    
    return False

def kolla_online(password):
    """
    Kollar hashen av lösenordet mot Have I Been Pwned API.
    Returnerar antal träffar (int).
    """
    # Skapar SHA-1 hash (krav från API:et)
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # Delar upp hashen för k-anonymitet (skickar bara prefix)
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        # Hämtar data med urllib (standard i Python)
        with urllib.request.urlopen(url, timeout=5) as response:
            # Läser svaret och gör om det till text
            data = response.read().decode('utf-8')
            
            # Loopar igenom svaret textrad för textrad
            for line in data.splitlines():
                hash_del, count = line.split(':')
                
                # Jämför suffixet från API med mitt eget
                if hash_del == suffix:
                    return int(count)
    except Exception:
        print("[-] Kunde inte nå servern för online-koll.")
        logging.error("Kunde inte nå HIBP-servern.")
    
    return 0

def kolla_comb(password):
    """
    Kollar lösenordet mot ProxyNova COMB-databasen.
    Returnerar antal träffar (int).
    """
    # Bygger upp URL:en med lösenordet som sökfråga
    url = f"https://api.proxynova.com/comb?query={password}&limit=1"
    
    try:
        # Skapar en request med User-Agent header (API:et kräver detta)
        req = urllib.request.Request(url, headers={'User-Agent': 'curl'})
        
        # Hämtar data från API:et
        with urllib.request.urlopen(req, timeout=5) as response:
            # Läser JSON-svaret
            data = json.loads(response.read().decode('utf-8'))
            
            # Räknar hur många gånger lösenordet hittades
            count = data.get('count', 0)
            return count
    except Exception:
        print("[-] Kunde inte nå ProxyNova COMB-servern.")
        logging.error("Kunde inte nå COMB-servern.")
    
    return 0

def visa_meny():
    """
    Visar huvudmenyn och returnerar användarens val.
    """
    print("\n=== HUVUDMENY ===")
    print("1. Kolla lösenord offline (endast lokala ordlistor)")
    print("2. Kolla lösenord online (endast internet)")
    print("3. Kolla lösenord fullständigt (lokala ordlistor + internet)")
    print("4. Avsluta programmet")
    print("==================")
    
    val = input("\nVälj ett alternativ (1-4): ")
    return val

def main():
    # --- KONFIGURATION FÖR LOGGNING ---
    # Sparar tidpunkt, nivå och meddelande i filen nyckelkollen.log
    logging.basicConfig(
        filename='nyckelkollen.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # --- SYSTEMKONTROLL ---
    print("--- Startar kontroll av systemet ---")
    
    # Här kör vi kollen (Nytt för att klara VG-krav)
    if not system_koll():
        print("[-] Avbryter programmet eftersom systemkraven inte uppfylldes.")
        return

    current_os = platform.system()
    print(f"Ditt operativsystem: {current_os}")
    logging.info(f"Programmet startades på: {current_os}")
    
    # --- INPUT FRÅN ANVÄNDARE ---
    print("\nLösenordskoll v3.1")
    
    # Visar menyn och får användarens val
    val = visa_meny()
    logging.info(f"Användaren valde menyalternativ: {val}")
    
    # Om användaren vill avsluta direkt
    if val == "4":
        print("\nAvslutar programmet. Hej då!")
        logging.info("Användaren avslutade programmet.")
        return
    
    # Kontrollera att valet är giltigt
    if val not in ["1", "2", "3"]:
        print("\nFel: Ogiltigt val. Välj 1, 2, 3 eller 4.")
        logging.warning("Ogiltigt menyval gjordes.")
        return
    
    # Fråga efter lösenord
    user_password = input("\nSkriv in lösenordet du vill testa: ")
    
    if user_password:
        print("\nLösenordet mottaget.")
        print(f"Längd: {len(user_password)} tecken.")
        logging.info(f"Testar lösenord med längd: {len(user_password)}")
        
        # --- KONTROLL 1: LOKAL MAPP (endast för alternativ 1 och 3) ---
        if val in ["1", "3"]:
            print("\nAnalysera mot lokala ordlistor...")
            finns_i_lista = kolla_mapp(user_password)
            
            if finns_i_lista:
                print("[!] VARNING: Lösenordet hittades i en av dina ordlistor.")
                logging.warning("Träff i lokal ordlista!")
            else:
                print("[+] Lösenordet hittades inte i någon av de skannade listorna.")
                logging.info("Ingen träff i lokala listor.")
        
        # --- KONTROLL 2 & 3: ONLINE (för alternativ 2 och 3) ---
        if val in ["2", "3"]:
            # --- KONTROLL 2: ONLINE-API ---
            print("\nKör kontroll mot online-databas...")
            antal_traffar = kolla_online(user_password)
            
            if antal_traffar > 0:
                print(f"[!] VARNING: Lösenordet har läckt {antal_traffar} gånger online (HIBP).")
                logging.warning(f"HIBP-träff: {antal_traffar} gånger.")
                
                print("    -> Rekommendation: Byt lösenord omedelbart.")
                print("    -> INFO: Lösenordet är komprometterat och bör betraktas som förbrukat.")
            else:
                print("[+] Grönt ljus! Inga träffar i onlinedatabasen.")
                logging.info("Ingen träff i HIBP.")
            
            # --- KONTROLL 3: COMB-DATABAS ---
            print("\nKör kontroll mot COMB-databasen...")
            antal_comb = kolla_comb(user_password)
            
            if antal_comb > 0:
                print(f"[!] VARNING: Lösenordet hittades {antal_comb} gånger i COMB-databasen.")
                logging.warning(f"COMB-träff: {antal_comb} gånger.")
                
                print("    -> Rekommendation: Byt lösenord omedelbart.")
                if antal_comb >= 10000:
                    print("    -> KRITISKT: Databasen visar max 10 000 träffar. Det verkliga antalet är sannolikt mycket högre.")
                else:
                    print("    -> INFO: Lösenordet är komprometterat och bör betraktas som förbrukat.")
            else:
                print("[+] Grönt ljus! Inga träffar i COMB-databasen.")
                logging.info("Ingen träff i COMB.")
                
        logging.info("Analys slutförd.")
    else:
        print("\nFel: Inget lösenord angavs.")
        logging.error("Inget lösenord angavs.")

if __name__ == "__main__":
    main()