Övning 2: Lösenordsknäckning med Hashcat

Syftet med denna övning är att förstå varför långa lösenord är mer säkra mot rainbow tables. Vi ska bevisa detta genom att visa hur Hashcats mask-attack tar längre tid ju längre det numeriska lösenordet är.

Filer och Deras Syfte:

md5-hasher.py: Detta Python-script skapar 10 st slumpmässiga numeriska hashar som är för långa för att knäckas av enkla rainbow tables.

[hashfil].txt: Detta är filen med hasharna som ska användas som inmatningsdata till Hashcat.

md5-hashcat.sh: Detta Bash-script startar knäckningsattacken. Den använder Hashcat för att testa en mask mot hasharna.

screenshot.jpg: En bild som bevisar att knäckningen lyckades, där Hashcat visar Status: Cracked och Recovered 10/10.

Körning: 

För att utföra attacken kör du scriptet med hashfilen och rätt numerisk mask (?d):

./md5-hashcat.sh [hashfil] [mask]
