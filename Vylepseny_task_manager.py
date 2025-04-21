import mysql.connector
from db import *

def hlavni_menu(connection):
    while True:
        print("\n📋 Správce úkolů - Hlavní menu")
        print("\n1️⃣. Přidat nový úkol")
        print("2️⃣. Zobrazit všechny úkoly")
        print("3️⃣. Aktualizovat úkol")
        print("4️⃣. Odstranit úkol")
        print("5️⃣. Konec programu")
        
        try:
            volba=int(input("\nVyberte možnost (1-4):\n"))
            if volba == 1:
                nazev = input("\nZadejte název úkolu: ").strip()
                popis = input("Zadejte popis úkolu: ").strip()
                pridat_ukol(connection, nazev, popis)
            elif volba == 2:
                zobrazit_vsechny_ukoly(connection)
            elif volba == 3:
                zobrazit_vsechny_ukoly(connection)
                ukol_id = int(input("Vyberte úkol dle ID, který chtete aktualizovat.\n"))
                aktualizovat_ukol(connection, ukol_id)
            elif volba == 4:
                zobrazit_vsechny_ukoly(connection)
                ukol_id = int(input("Vyberte úkol dle ID, který chtete odstranit.\n"))
                odstranit_ukol(connection, ukol_id)
            elif volba == 5:
                print("👋 Konec programu 👋")
                break
            else:
                print("\nToto je špatná volba, prosím, opakujte výběr:")
        except ValueError:
            print("❌ Zadejte číslo od 1 do 4.")

def pridat_ukol(connection,nazev, popis,test_mode=False):
    if nazev == "" or popis == "":
        print("\nNevyplnili jste název nebo popis úkolu, opakujte akci:\n")
    else:
        pridat_ukol_db(connection, nazev, popis)

def zobrazit_vsechny_ukoly(connection,test_mode=False):
    ukolyDb = vrat_vsechny_ukoly_db(connection, test_mode)
    if not ukolyDb:
        print ("Žádný úkol není k dispozici.")

    for ukol in ukolyDb:
        stav = "🟡" if ukol[3] == "probíhá" else "🔴" if ukol[3] == "nezahájeno" else "✅"
        print(f"ID:{ukol[0]} {stav}{ukol[3]} {ukol[1]} - {ukol[2]}")
        

def aktualizovat_ukol(connection, ukol_id,test_mode=False):
    ukol = vrat_ukol_db(ukol_id, connection, test_mode)
    if not ukol:
        print("Ukol s tímto ID neexistuje, zkuste to znovu.")

    else:
        novy_stav = int(input("Zmáčkněte 1️⃣ pro nový stav Probíhá nebo 2️⃣ pro nový stav Hotovo\n"))
        if novy_stav != 1 and novy_stav != 2:
            print("Zadali jste nesprávný stav.")
        else:
            stav= "Probíhá"
        if novy_stav == 2:
            stav= "Hotovo"

        aktualizuj_ukol_db(ukol_id, stav, connection, test_mode)
        print ("\nÚkol aktualizován.")

def odstranit_ukol(connection,ukol_id, test_mode=False):  
    ukol = vrat_ukol_db(ukol_id, connection, test_mode)

    if not ukol:
        print("Ukol s tímto ID neexistuje, zkuste to znovu.")
    
    smaz_ukol_db(ukol_id, connection, test_mode)

connection = pripojeni_db()

vytvoreni_tabulky(connection)
hlavni_menu(connection)




