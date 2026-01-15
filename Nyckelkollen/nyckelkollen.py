#!/usr/bin/env python3
import platform       # För att kolla vilket operativsystem som körs
import os             # För att hantera filer och mappar i systemet
import hashlib        # För att skapa säkra hash-summor av lösenord
import urllib.request # För att kunna hämta data från internet (API)
import urllib.error   # För att hantera specifika urllib-fel
import json           # För att tolka JSON-svar från API:er
import logging        # För att logga händelser och fel till fil
import argparse       # För att hantera flaggor och argument i terminalen
import sys            # För att rensa skärmen på rätt sätt

# Global variabel för version
VERSION = "3.5"

# ANSI-färgkoder för terminal
class Farg:
    ROD = '\033[91m'
    GRON = '\033[92m'
    GUL = '\033[93m'
    BLA = '\033[94m'
    RESET = '\033[0m'
    FET = '\033[1m'

def rensa_skarm():
    """Rensar terminalfönstret."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def skriv_rubrik(text):
    """Skriver ut en snygg rubrik."""
    print(f"\n{Farg.FET}{Farg.BLA}{'=' * 50}{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}{text.center(50)}{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}{'=' * 50}{Farg.RESET}\n")

def system_koll():
    """
    Kollar att systemet uppfyller kraven innan start.
    1. Kollar skrivrättigheter (för loggfilen).
    2. Kollar internetanslutning (för API:er).
    Returnerar tuple: (skrivrättigheter_ok, internet_ok)
    """
    # Test 1: Skrivrättigheter i nuvarande mapp
    if not os.access(".", os.W_OK):
        print("[-] Fel: Saknar skrivrättigheter i mappen. Kan inte skapa loggfil.")
        return (False, False)

    # Test 2: Internetanslutning (försöker nå Google snabbt)
    internet_ok = True
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
    except Exception:
        print("[-] Varning: Ingen internetanslutning. Online-kontroller kommer inte att fungera.")
        internet_ok = False

    return (True, internet_ok)

def analysera_komplexitet(password):
    """
    Analyserar lösenordets struktur (längd, teckentyper).
    Ger direkt feedback till användaren om lösenordet följer 'best practice'.
    """
    skriv_rubrik("STRUKTURANALYS")
    
    svagheter = []
    
    # Kriterium 1: Längd
    if len(password) < 8:
        svagheter.append(f"Kritiskt kort längd ({len(password)} tecken). Bör vara minst 12.")
    elif len(password) < 12:
        svagheter.append(f"Ganska kort ({len(password)} tecken). Rekommenderas minst 12 för hög säkerhet.")

    # Kriterium 2-5: Teckentyper
    if not any(c.isupper() for c in password):
        svagheter.append("Saknar stora bokstäver (A-Z).")
    if not any(c.islower() for c in password):
        svagheter.append("Saknar små bokstäver (a-z).")
    if not any(c.isdigit() for c in password):
        svagheter.append("Saknar siffror (0-9).")
    if all(c.isalnum() for c in password):
        svagheter.append("Saknar specialtecken (t.ex. !, @, #, $).")

    # Skriv ut resultatet
    if svagheter:
        print(f"{Farg.ROD}✗ Lösenordet har strukturella svagheter:{Farg.RESET}")
        for punkt in svagheter:
            print(f"{Farg.ROD}  • {punkt}{Farg.RESET}")
        logging.warning(f"Komplexitetsanalys: Hittade {len(svagheter)} svagheter.")
    else:
        print(f"{Farg.GRON}✓ Lösenordet har en stark struktur (blandade tecken och god längd).{Farg.RESET}")
        logging.info("Komplexitetsanalys: Godkänd struktur.")

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

def visa_meny(felmeddelande=None, visa_system_info=False, os_info=None, internet_status=None):
    """
    Visar huvudmenyn och returnerar användarens val.
    Kan visa felmeddelande och systeminformation.
    """
    rensa_skarm()
    print(f"\n{Farg.FET}{Farg.BLA}╔{'═' * 56}╗{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}║{' ' * 56}║{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}║{'NYCKELKOLLEN'.center(56)}║{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}║{f'Version {VERSION}'.center(56)}║{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}║{f'OS: {os_info}'.center(56)}║{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}║{' ' * 56}║{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}╚{'═' * 56}╝{Farg.RESET}\n")
    
    # Visa varning om internet saknas vid uppstart
    if visa_system_info and not internet_status:
        print(f"{Farg.GUL}OBS: Endast offline-läge (alternativ 1) kommer att fungera.{Farg.RESET}")
        print()
    
    # Visa felmeddelande om det finns
    if felmeddelande:
        print(f"{Farg.ROD}{felmeddelande}{Farg.RESET}\n")
    
    print(f"{Farg.FET}{Farg.BLA}╔{'═' * 56}╗{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}║{'HUVUDMENY'.center(56)}║{Farg.RESET}")
    print(f"{Farg.FET}{Farg.BLA}╚{'═' * 56}╝{Farg.RESET}\n")
    print(f"{Farg.FET}1.{Farg.RESET} Kolla lösenord offline (endast lokala ordlistor)")
    print(f"{Farg.FET}2.{Farg.RESET} Kolla lösenord online (endast internet)")
    print(f"{Farg.FET}3.{Farg.RESET} Kolla lösenord fullständigt (lokala ordlistor + internet)")
    print(f"{Farg.FET}4.{Farg.RESET} Avsluta programmet")
    print(f"\n{Farg.BLA}{'─' * 58}{Farg.RESET}")
    
    val = input(f"\n{Farg.FET}Välj ett alternativ (1-4):{Farg.RESET} ")
    return val

def visa_sammanfattning(resultat):
    """
    Visar en snygg sammanfattning av alla kontroller.
    resultat är en dict med: {'struktur': bool, 'lokal': bool/None, 'online': int/None}
    """
    skriv_rubrik("SAMMANFATTNING")
    
    totalt_sakert = True
    
    # Strukturanalys
    if resultat['struktur']:
        print(f"{Farg.GRON}✓ Strukturanalys:{Farg.RESET} Godkänd")
    else:
        print(f"{Farg.ROD}✗ Strukturanalys:{Farg.RESET} Svagheter upptäckta")
        totalt_sakert = False
    
    # Lokal kontroll
    if resultat['lokal'] is not None:
        if resultat['lokal']:
            print(f"{Farg.ROD}✗ Lokal ordlista:{Farg.RESET} Lösenordet hittades i ordlista")
            totalt_sakert = False
        else:
            print(f"{Farg.GRON}✓ Lokal ordlista:{Farg.RESET} Ingen träff")
    
    # Online kontroll
    if resultat['online'] is not None:
        if resultat['online'] > 0:
            print(f"{Farg.ROD}✗ Online-databas:{Farg.RESET} Läckt {resultat['online']} gånger")
            totalt_sakert = False
        else:
            print(f"{Farg.GRON}✓ Online-databas:{Farg.RESET} Ingen träff")
    
    # Slutgiltig bedömning
    print(f"\n{Farg.BLA}{'─' * 50}{Farg.RESET}")
    if totalt_sakert:
        print(f"{Farg.FET}{Farg.GRON}RESULTAT: Lösenordet verkar säkert! ✓{Farg.RESET}")
    else:
        print(f"{Farg.FET}{Farg.ROD}RESULTAT: Lösenordet bör bytas omedelbart! ✗{Farg.RESET}")
    print(f"{Farg.BLA}{'─' * 50}{Farg.RESET}\n")

def main():
    # --- INSTÄLLNINGAR FÖR ARGUMENT ---
    parser = argparse.ArgumentParser(
        prog='Nyckelkollen',
        description='Nyckelkollen - Ett professionellt verktyg för att kontrollera lösenordssäkerhet.',
        epilog='Utvecklat för att hjälpa användare att identifiera svaga och komprometterade lösenord.'
    )
    parser.add_argument("-v", "--version", action="store_true", 
                       help="Visar programmets version och information")
    
    args = parser.parse_args()

    # Om flaggan för version anges, skriv ut och avslyta
    if args.version:
        print(f"\n{Farg.FET}{Farg.BLA}{'=' * 50}{Farg.RESET}")
        print(f"{Farg.FET}{Farg.BLA}Nyckelkollen - Lösenordssäkerhetsverktyg{Farg.RESET}")
        print(f"{Farg.FET}{Farg.BLA}{'=' * 50}{Farg.RESET}\n")
        print(f"Version: {Farg.GRON}{VERSION}{Farg.RESET}")
        print(f"Skapad för att analysera lösenordssäkerhet genom:")
        print(f"  • Strukturanalys (längd, teckentyper)")
        print(f"  • Lokala ordlistor (offline)")
        print(f"  • Have I Been Pwned API (online)")
        print(f"\nAnvändning: python3 nyckelkollen.py")
        print(f"           python3 nyckelkollen.py --version")
        print(f"           python3 nyckelkollen.py --help\n")
        return

    # --- KONFIGURATION FÖR LOGGNING ---
    # Sparar tidpunkt, nivå och meddelande i filen nyckelkollen.log
    logging.basicConfig(
        filename='nyckelkollen.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # --- SYSTEMKONTROLL ---
    skriv_ok, internet_ok = system_koll()
    if not skriv_ok:
        print("[-] Avbryter programmet eftersom systemkraven inte uppfylldes.")
        return

    current_os = platform.system()
    logging.info(f"Programmet startades på: {current_os}")
    
    if not internet_ok:
        logging.warning("Programmet startades utan internetanslutning.")
    
    # --- HUVUDLOOP SOM TILLÅTER FLERA KÖRNINGAR ---
    felmeddelande = None
    forsta_gangen = True
    
    while True:
        # --- INPUT FRÅN ANVÄNDARE ---
        
        # Visar menyn och får användarens val
        val = visa_meny(felmeddelande, forsta_gangen, current_os, internet_ok)
        forsta_gangen = False
        felmeddelande = None
        logging.info(f"Användaren valde menyalternativ: {val}")
        
        # Om användaren vill avsluta direkt
        if val == "4":
            print("\nAvslutar programmet. Hej då!")
            logging.info("Användaren avslutade programmet.")
            break
        
        # Kontrollera att valet är giltigt
        if val not in ["1", "2", "3"]:
            felmeddelande = "Fel: Ogiltigt val. Välj 1, 2, 3 eller 4."
            logging.warning("Ogiltigt menyval gjordes.")
            continue
        
        # Kontrollera om användaren valde online-alternativ utan internet
        if not internet_ok and val in ["2", "3"]:
            felmeddelande = "Fel: Du saknar internetanslutning. Endast alternativ 1 (offline) är tillgängligt."
            logging.error("Försök att använda online-funktioner utan internet.")
            continue
        
        # Fråga efter lösenord
        user_password = input("\nSkriv in lösenordet du vill testa: ")
        
        if user_password:
            rensa_skarm()
            print(f"\n{Farg.BLA}Lösenordet mottaget. Längd: {len(user_password)} tecken.{Farg.RESET}")
            logging.info(f"Testar lösenord med längd: {len(user_password)}")
            
            # Dictionary för att spara resultat
            resultat = {'struktur': False, 'lokal': None, 'online': None}
            
            # --- ANALYSERA STRUKTUR (Komplexitet) ---
            # Enkel check för struktur
            if len(user_password) >= 12 and any(c.isupper() for c in user_password) and \
               any(c.islower() for c in user_password) and any(c.isdigit() for c in user_password) and \
               not all(c.isalnum() for c in user_password):
                resultat['struktur'] = True
            
            analysera_komplexitet(user_password)
            
            # --- KONTROLL 1: LOKAL MAPP ---
            if val in ["1", "3"]:
                skriv_rubrik("LOKAL ORDLISTEKONTROLL")
                print(f"{Farg.BLA}Söker igenom lokala ordlistor...{Farg.RESET}")
                finns_i_lista = kolla_mapp(user_password)
                resultat['lokal'] = finns_i_lista
                
                if finns_i_lista:
                    print(f"\n{Farg.ROD}✗ VARNING: Lösenordet hittades i en av dina ordlistor.{Farg.RESET}")
                    logging.warning("Träff i lokal ordlista!")
                else:
                    print(f"\n{Farg.GRON}✓ Lösenordet hittades inte i de skannade listorna.{Farg.RESET}")
                    logging.info("Ingen träff i lokala listor.")
            
            # --- KONTROLL 2: ONLINE ---
            if val in ["2", "3"]:
                skriv_rubrik("ONLINE-KONTROLL (HIBP)")
                print(f"{Farg.BLA}Kontrollerar mot Have I Been Pwned...{Farg.RESET}")
                antal_traffar = kolla_online(user_password)
                resultat['online'] = antal_traffar
                
                if antal_traffar > 0:
                    print(f"\n{Farg.ROD}✗ KRITISKT: Lösenordet har läckt {antal_traffar} gånger i dataintrång.{Farg.RESET}")
                    print(f"{Farg.ROD}  Angripare kan ha tillgång till detta lösenord - byt omedelbart!{Farg.RESET}")
                    logging.warning(f"HIBP-träff: {antal_traffar} gånger.")
                else:
                    print(f"\n{Farg.GRON}✓ Inga träffar i onlinedatabasen.{Farg.RESET}")
                    logging.info("Ingen träff i HIBP.")
            
            # --- VISA SAMMANFATTNING ---
            visa_sammanfattning(resultat)
            
            logging.info("Analys slutförd.")
            
            # Fråga om användaren vill köra igen med felhantering
            while True:
                print(f"\n{Farg.BLA}{'─' * 50}{Farg.RESET}")
                igen = input(f"{Farg.FET}Vill du testa ett annat lösenord? (j/n):{Farg.RESET} ").lower().strip()
                
                if igen in ['j', 'ja']:
                    logging.info("Användaren valde att testa ett nytt lösenord.")
                    break
                elif igen in ['n', 'nej']:
                    print("\nAvslutar programmet. Hej då!")
                    logging.info("Användaren valde att avsluta efter analys.")
                    return
                else:
                    print(f"{Farg.ROD}Ogiltigt svar. Svara 'j' för ja eller 'n' för nej.{Farg.RESET}")
        else:
            felmeddelande = "Fel: Inget lösenord angavs."
            logging.error("Inget lösenord angavs.")

if __name__ == "__main__":
    main()