import sqlite3

def posodobi_bazo():
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    
    try:
        # Dodamo nov stolpec v tabelo (če se koda izvede večkrat, bo to preprečilo napako)
        cursor.execute("ALTER TABLE trades ADD COLUMN tip_trejda TEXT DEFAULT 'zgodovina'")
        print("✅ Stolpec 'tip_trejda' uspešno dodan v bazo.")
    except sqlite3.OperationalError:
        print("ℹ️ Stolpec 'tip_trejda' že obstaja. Baza je pripravljena.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    posodobi_bazo()