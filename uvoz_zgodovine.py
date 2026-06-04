import sqlite3
import pandas as pd
import glob
import os

def uvozi_zgodovino():
    # Povežemo se z bazo
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()

    # 1. Čiščenje starih (testnih) podatkov
    print("Brišem stare podatke iz baze...")
    cursor.execute('DELETE FROM trades')
    conn.commit()

    # 2. Iskanje vseh CSV datotek v trenutni mapi
    csv_datoteke = glob.glob('*.csv')
    
    uspesno_uvozenih = 0

    for datoteka in csv_datoteke:
        try:
            # Preberemo datoteko
            df = pd.read_csv(datoteka)
            
            # Preverimo, če je to prava datoteka (mora imeti stolpec 'Trade number')
            if 'Trade number' not in df.columns:
                print(f"Preskakujem {datoteka} (ni pravi format - nima seznama trejdov).")
                continue
                
            print(f"Uvažam podatke iz: {datoteka} ...")
            
            # Grupiramo po Trade number (da združimo Entry in Exit iz TradingView-a v en trejd)
            for trade_id, group in df.groupby('Trade number'):
                entry_row = group[group['Type'].str.contains('Entry', case=False, na=False)]
                exit_row = group[group['Type'].str.contains('Exit', case=False, na=False)]
                
                if entry_row.empty:
                    continue
                
                # Podatki o vstopu v trejd
                entry_time = entry_row.iloc[0]['Date and time']
                entry_price = entry_row.iloc[0]['Price USDT']
                pos_size = entry_row.iloc[0]['Size (qty)']
                capital = entry_row.iloc[0]['Size (value)']
                
                # Ime strategije potegnemo iz "Signal" in malce očistimo
                signal = str(entry_row.iloc[0]['Signal']).replace('LONG ', '').replace('SHORT ', '') 
                
                # Podatki o izstopu (če je trejd že zaključen)
                if not exit_row.empty:
                    exit_time = exit_row.iloc[0]['Date and time']
                    pnl = exit_row.iloc[0]['Net PnL USD']
                    status = 'closed'
                else:
                    # Če exit ne obstaja, gre za trenutno odprto pozicijo
                    exit_time = None
                    pnl = 0.0
                    status = 'open'
                
                # Zapis v najino SQL bazo
                cursor.execute('''
                INSERT INTO trades (strategy_name, symbol, entry_price, position_size, capital_used, status, pnl, entry_time, exit_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (signal, 'BTC/USDT', entry_price, pos_size, capital, status, pnl, entry_time, exit_time))
                
                uspesno_uvozenih += 1
                
        except Exception as e:
            print(f"Napaka pri branju datoteke {datoteka}: {e}")

    conn.commit()
    conn.close()
    print(f"\n✅ Uspešno uvoženih {uspesno_uvozenih} pravih trejdov iz tvojih strategij v bazo!")

if __name__ == "__main__":
    uvozi_zgodovino()