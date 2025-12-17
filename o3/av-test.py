#!/usr/bin/env python3

import platform
import time

# 1. Kontrollera operativsystem
system = platform.system()

if system == "Windows":
    print("Windows upptäckt. Scriptet fortsätter.")

elif system == "Linux":
    print("Linux upptäckt. Detta script är avsett för Windows.")
    exit()

elif system == "Darwin":
    print("macOS upptäckt. Detta script är avsett för Windows.")
    exit()

else:
    print(f"Okänt operativsystem ({system}). Detta script är avsett för Windows.")
    exit()

# 2. Inställningar
# Definerar sögväg och namnet på filen
filnamn = r"C:\Users\Max\Desktop\AV-TEST-NOT-DANGEROUS.txt"

# EICAR-strängen (ofarlig teststräng)
eicar_str = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# 3. Skapa filen
try:
    with open(filnamn, "w") as f:
        f.write(eicar_str)
    print(f"Fil skapad på: {filnamn}")
except:
    print("Kunde inte skapa filen. Kontrollera att sökvägen är rätt.")
    exit()

# 4. Vänta på att Antivirus ska reagera
print("Väntar 3 sekunder...")
time.sleep(3)

# 5. Kontrollera resultatet
try:
    # Försök läsa filen
    with open(filnamn, "r") as f:
        innehåll = f.read()

    # Om vi kan läsa filen, kolla om texten är kvar
    if innehåll == eicar_str:
        print("Filen finns kvar. Antivirus reagerade inte.")
    else:
        print("Filen finns kvar, men innehållet har ändrats.")

except:
    # Om filen inte går att öppna (för att AV tog bort den) hamnar vi här
    print("Filen kunde inte läsas!")
    print("Antivirus har troligen tagit bort filen.")
    print("Testet lyckades. Din antivirus-lösning fungerar.")
