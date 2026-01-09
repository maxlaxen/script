#!/usr/bin/env python3
import platform       # För att kolla vilket operativsystem som körs
import os             # För att hantera filer och mappar i systemet
import hashlib        # För att skapa säkra hash-summor av lösenord
import urllib.request # För att kunna hämta data från internet (API)
import json           # För att tolka JSON-svar från API:er

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
    
    return 0

def main():
    # --- SYSTEMKONTROLL ---
    print("--- Startar kontroll av systemet ---")
    
    current_os = platform.system()
    print(f"Ditt operativsystem: {current_os}")
    
    # --- INPUT FRÅN ANVÄNDARE ---
    print("\nLösenordskoll v2.0")
    
    user_password = input("Skriv in lösenordet du vill testa: ")
    
    if user_password:
        print("\nLösenordet mottaget.")
        print(f"Längd: {len(user_password)} tecken.")
        
        # --- KONTROLL 1: LOKAL MAPP ---
        print("\nAnalysera mot lokala ordlistor...")
        finns_i_lista = kolla_mapp(user_password)
        
        if finns_i_lista:
            print("[!] VARNING: Lösenordet hittades i en av dina ordlistor.")
        else:
            print("[+] Lösenordet hittades inte i någon av de skannade listorna.")
        
        # --- KONTROLL 2: ONLINE-API ---
        print("\nKör kontroll mot online-databas...")
        antal_traffar = kolla_online(user_password)
        
        if antal_traffar > 0:
            print(f"[!] VARNING: Lösenordet har läckt {antal_traffar} gånger online (HIBP).")
        else:
            print("[+] Grönt ljus! Inga träffar i onlinedatabasen.")
        
        # --- KONTROLL 3: COMB-DATABAS ---
        print("\nKör kontroll mot COMB-databasen...")
        antal_comb = kolla_comb(user_password)
        
        if antal_comb > 0:
            print(f"[!] VARNING: Lösenordet hittades {antal_comb} gånger i COMB-databasen.")
        else:
            print("[+] Grönt ljus! Inga träffar i COMB-databasen.")
    else:
        print("\nFel: Inget lösenord angavs.")

if __name__ == "__main__":
    main()