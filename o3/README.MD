# Övning 3 - AV/EDR Malware Test

1. Scriptet kontrollerar först om operativsystemet är Windows.
2. Det skapar en fil med en EICAR-testsignatur, vilket är ett ofarligt "virus" som alla antivirusprogram ska upptäcka.
3. Scriptet väntar i 3 sekunder för att låta antiviruset reagera och hantera filen.
4. Scriptet försöker läsa filen igen för att kontrollera om antiviruset har tagit bort eller karantäniserat den.
5. Skärmbilden är ett exempel som visar hur händelsen ser ut när den registreras i Windows Loggbok.

## Användning
Kör scriptet i Windows med: python av-test.py
