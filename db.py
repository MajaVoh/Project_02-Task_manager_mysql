import mysql.connector
from mysql.connector import Error

def pripojeni_db(): 
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Matysek55!",
            database = "projekt_db"
        )
        return connection
    except: 
        print("Připojení k databázi se nepovedlo.")
        return None

def vytvoreni_tabulky(connection, test_mode=False):
    try:
        table_name = "ukoly_test" if test_mode else "ukoly"
        cursor = connection.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR (50) NOT NULL,
                    popis VARCHAR (50) NOT NULL,
                    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno', 
                    datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
                )
        '''
        )   
        print("Tabulka byla vytvořena.")
    except mysql.connector.Error as err:
        print(f"🛑 Chyba při vytváření tabulky: {err}")
    connection.commit()
    cursor.close()

def pridat_ukol_db(connection, nazev, popis, test_mode=False):
    table_name = "ukoly_test" if test_mode else "ukoly"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table_name} (nazev, popis) VALUES (%s, %s)",(nazev, popis))
    connection.commit()
    cursor.close()

def vrat_vsechny_ukoly_db(connection, test_mode=False):
    try:
        cursor = connection.cursor()
        table_name = "ukoly_test" if test_mode else "ukoly"
        cursor.execute(f"SELECT id, nazev, popis, stav, datum_vytvoreni FROM {table_name} WHERE stav IN (%s, %s)", ("Nezahájeno", "Probíhá"))
        ukolyDb = cursor.fetchall()
        connection.commit()
        cursor.close()
        return ukolyDb
    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")    
        return None
    
def vrat_ukol_db(ukol_id, connection, test_mode=False):
    try:
        cursor = connection.cursor()
        table_name = "ukoly_test" if test_mode else "ukoly"
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s",( ukol_id,))
        ukol=cursor.fetchone()
        return ukol
    except mysql.connector.Error as err:
        print(f"Chyba při ziskávání ukolu: {err}")    
        return None
    
def aktualizuj_ukol_db(ukol_id, stav, connection, test_mode=False):
    try:
        cursor = connection.cursor()
        table_name = "ukoly_test" if test_mode else "ukoly"
        cursor.execute(f"UPDATE {table_name} SET stav = %s WHERE id = %s",(stav, ukol_id))
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Chyba aktualizaci ukolu: {err}")    
        return None
    
def smaz_ukol_db(ukol_id, connection, test_mode=False):
    try:
        cursor = connection.cursor()
        table_name = "ukoly_test" if test_mode else "ukoly"
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s",(ukol_id,))
        connection.commit()
        cursor.close()
        print("Úkol byl smazán.")

    except mysql.connector.Error as err:
        print(f"Chyba při mazání dat: {err}")
        return None