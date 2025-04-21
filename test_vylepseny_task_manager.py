import mysql.connector
import pytest
from db import pripojeni_db, vytvoreni_tabulky, pridat_ukol_db, aktualizuj_ukol_db, smaz_ukol_db

@pytest.fixture()
def connection():
    connection = pripojeni_db()
    vytvoreni_tabulky(connection, test_mode=True)
    yield connection

    cursor = connection.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS ukoly_test")
        connection.commit()
    except mysql.connector.Error as e:
        print(f"⚠️ Chyba při mazání testovací tabulky: {e}")
    cursor.close()
    connection.close()
        
def test_pridat_ukol(connection):
    nazev= "test ukol"
    popis= "test popis"

    pridat_ukol_db(connection,nazev, popis, test_mode=True)
    cursor=connection.cursor()
    cursor.execute ("SELECT * FROM ukoly_test WHERE nazev = %s and popis = %s;",(nazev, popis))
    result = cursor.fetchone()

    assert result is not None

    nazev = None
    popis = None

    try:
        pridat_ukol_db(connection, nazev, popis, test_mode=True)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ukoly_test WHERE nazev = %s AND popis = %s", (nazev, popis))
        result = cursor.fetchone()

    except mysql.connector.Error as err:
        assert err.errno == 1048

def test_aktualizovat_ukol(connection,test_mode=True):
    pridat_ukol_db(connection, "test nazev", "test popis", test_mode=True)
    aktualizuj_ukol_db(1, "hotovo",connection,test_mode=True)
    cursor=connection.cursor()
    cursor.execute("SELECT stav FROM ukoly_test WHERE id = %s", [1])
    result = cursor.fetchone()
    assert result[0] == "Hotovo"

    result = aktualizuj_ukol_db(1, "neplatny_stav",connection,test_mode=True)
    assert result is None

def test_smaz_ukol(connection,test_mode=True):
    pridat_ukol_db(connection, "test nazev", "test popis", test_mode=True)
    smaz_ukol_db(1,connection,test_mode=True)
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM ukoly_test")
    result = cursor.fetchall()

    assert len(result) == 0

    result = smaz_ukol_db('abc',connection,test_mode=True)
    assert result is None




    
