#!/bin/bash
#
# Detta script samlar in systeminformation - RECON
#
# Kan användas för följande attacker:
# [Skriv möjliga attacker]
#
# Author: Frans Schartau
# Last Update: 2025-01-01

echo "Välkommen till mitt RECON script för att kontrollera en Linux-miljö"

echo
echo "=== SYSTEMINFO ==="
uname -a

echo
echo "=== AKTUELL ANVÄNDARE ==="
echo $USER

echo
echo "=== ANVÄNDARE MED SHELL ==="
grep "sh$" /etc/passwd

echo
echo "=== NÄTVERK ==="
ip a | grep inet

echo
echo "=== LÄGG TILL FLERA TESTER  ==="

#
# skriv in dina kommandon för tester
#
echo
echo "--- SYSTEM & HÅRDVARA ---"
echo "Datum och Tid:"
date
echo "Minnesstatus:"
free

echo
echo "--- PUBLIK IP & ÖPPNA PORTAR ---"
echo "Publik IP-adress:"
# Använder curl för att hämta den publika IP-adressen
curl -s icanhazip.com 
echo "Lokala öppna portar:"
ss -tuln

echo
echo "--- SÖKVÄG TILL SKRIPT ---"
# Visar var scriptet körs ifrån
pwd

