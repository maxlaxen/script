import platform  # Bibliotek för att kunna läsa av systeminfo

def main():
    # --- STEG 1: SYSTEMKOLL ---
    print("--- Startar kontroll av systemet ---")
    
    # Hämta namnet på operativsystemet (t.ex. Windows, Linux)
    current_os = platform.system()
    
    print(f"Ditt operativsystem: {current_os}")
    

    # --- STEG 2: INPUT FRÅN ANVÄNDARE ---
    print("Lösenordskoll v1.0")
    
    # Ta emot input från användaren och spara i en variabel
    user_password = input("Skriv in lösenordet du vill testa: ")

    # Kontrollera att variabeln inte är tom
    if user_password:
        print("\nLösenordet mottaget.")
        # Visa längden på lösenordet (bra för att se att mellanslag kom med)
        print(f"Längd: {len(user_password)} tecken.")
    else:
        print("\nFel: Du skrev inte in något lösenord.")

# Se till att main-funktionen bara körs om vi startar filen direkt
if __name__ == "__main__":
    main()