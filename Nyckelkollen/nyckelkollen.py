#!/usr/bin/env python3
import platform
import os

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

def main():
    # --- SYSTEMKONTROLL ---
    print("--- Startar kontroll av systemet ---")
    
    current_os = platform.system()
    print(f"Ditt operativsystem: {current_os}")
    
    # --- INPUT FRÅN ANVÄNDARE ---
    print("Lösenordskoll v1.0")
    
    user_password = input("Skriv in lösenordet du vill testa: ")

    if user_password:
        print("\nLösenordet mottaget.")
        print(f"Längd: {len(user_password)} tecken.")

        # --- KONTROLL MOT MAPP ---
        print("Analysera mot lokala ordlistor...")
        finns_i_lista = kolla_mapp(user_password)

        if finns_i_lista:
            print("[!] VARNING: Lösenordet hittades i en av dina ordlistor.")
        else:
            print("[+] Lösenordet hittades inte i någon av de skannade listorna.")

    else:
        print("\nFel: Inget lösenord angavs.")

if __name__ == "__main__":
    main()