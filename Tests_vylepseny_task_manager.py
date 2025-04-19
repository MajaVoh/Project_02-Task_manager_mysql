import mysql.connector
import pytest
from db import pripojeni_db, vytvoreni_tabulky, pridat_ukol_db

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
    resurt = cursor.fetchone()

    assert resurt is not None