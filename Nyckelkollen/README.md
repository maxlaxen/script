# Lösenordskollen (v3.3)

Välkommen till **Lösenordskollen**. Detta är ett säkerhetsverktyg utvecklat i Python för att utvärdera hur starka och säkra lösenord är. Syftet med projektet är att ge användaren en tydlig bild av lösenordets kvalitet genom att kombinera teknisk analys med sökningar i databaser över kända dataintrång.

## Funktioner

Programmet utför flera tester för att säkerställa att lösenordet håller hög säkerhet:

1.  **Analys av lösenordsstyrka:** Verktyget granskar direkt om lösenordet uppfyller viktiga krav på säkerhet, såsom längd, användning av siffror, specialtecken och blandade bokstäver.
2.  **Sökning i lokala ordlistor:** Kontrollerar om lösenordet finns med i vanliga listor över dåliga lösenord (t.ex. `rockyou.txt`) som ligger i mappen `ordlistor`.
3.  **Kontroll mot dataläckor (HIBP):** Använder API:et från *Have I Been Pwned* för att se om lösenordet har läckt ut på nätet. Sökningen sker säkert utan att hela lösenordet skickas iväg.
4.  **COMB-databasen:** Gör en extra kontroll mot databasen *Compilation of Many Breaches* för att fånga upp fler potentiella läckor.
5.  **Loggning:** Alla sökningar och resultat sparas i en loggfil för historik och felsökning.

## Systemkrav

För att kunna använda verktyget behöver du:
* **Python 3** installerat.
* En **internetuppkoppling** (krävs för att nå databaserna online).
* Skrivrättigheter i mappen (för att programmet ska kunna spara loggfilen).
* En mapp namngiven `ordlistor` i samma katalog (om du vill använda funktionen för lokala sökningar).

## Installation och användning

För att installera verktyget hämtar du koden direkt från GitHub med följande steg:

1.  **Hämta koden:**
    Öppna din terminal och kör detta kommando:
    ```bash
    git clone [https://github.com/maxlaxen/script.git](https://github.com/maxlaxen/script.git)
    ```

2.  **Gå till rätt mapp:**
    Navigera in i undermappen där appen ligger:
    ```bash
    cd script/Nyckelkollen
    ```

3.  **Förberedelser:**
    (Valfritt) Om du vill använda funktionen för lokal sökning, placera dina ordlistor i mappen `ordlistor`.

### Starta programmet
Kör scriptet med Python 3:

```bash
python3 nyckelkollen.py

### Flaggor och alternativ
Du kan använda följande argument för att styra programmet:

* `-h` eller `--help`: Visar hjälpmeny med exempel på användning.
* `-v` eller `--version`: Visar aktuell versionsinformation.

Exempel på körning:
```bash
python3 nyckelkollen.py --version