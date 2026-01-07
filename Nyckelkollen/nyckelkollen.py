#!/usr/bin/env python3
import platform

def kolla_lista(password):
    """
    Kollar om lösenordet finns i en lokal textfil.
    Returnerar True vid matchning, annars False.
    """
    filnamn = "vanliga_losenord.txt"
    
    try:
        # Öppnar filen med utf-8 för att klara svenska tecken
        with open(filnamn, "r", encoding="utf-8", errors="ignore") as fil:
            for rad in fil:
                # Rensar bort radbrytningar och jämför med lösenordet
                if rad.strip() == password:
                    return True
    except FileNotFoundError:
        print(f"[-] Systemfel: Hittade inte filen '{filnamn}'.")
    
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

        # --- KONTROLL MOT LISTA ---
        print("Analysera mot databas...")
        finns_i_lista = kolla_lista(user_password)

        if finns_i_lista:
            print("[!] VARNING: Lösenordet hittades i listan över vanliga lösenord.")
        else:
            print("[+] Lösenordet hittades inte i den lokala listan.")

    else:
        print("\nFel: Inget lösenord angavs.")

if __name__ == "__main__":
    main()