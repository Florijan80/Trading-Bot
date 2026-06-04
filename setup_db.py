import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def create_database():
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()

    # Tabela za strategije
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS strategies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )''')

    # Tabela za trejde (odprte in zaprte)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY,
        strategy_name TEXT,
        symbol TEXT,
        entry_price REAL,
        position_size REAL,
        capital_used REAL,
        status TEXT,
        pnl REAL,
        entry_time TIMESTAMP,
        exit_time TIMESTAMP
    )''')

    conn.commit()
    
    # Vnos testnih strategij
    strategies = [('RSI Breakout',), ('MACD Trend',), ('EMA Crossover',)]
    cursor.executemany('INSERT OR IGNORE INTO strategies (name) VALUES (?)', strategies)
    
    # Brisanje starih testnih trejdov (če skripto poženete večkrat)
    cursor.execute('DELETE FROM trades')

    # Simulacija zgodovine: ZAPRTI TREJDI
    now = datetime.now()
    closed_trades = [
        ('RSI Breakout', 'BTC/USDT', 60000, 0.05, 3000, 'closed', 150.50, now - timedelta(days=5), now - timedelta(days=4)),
        ('MACD Trend', 'ETH/USDT', 3000, 0.5, 1500, 'closed', -50.00, now - timedelta(days=4), now - timedelta(days=3)),
        ('RSI Breakout', 'SOL/USDT', 120, 10, 1200, 'closed', 80.20, now - timedelta(days=3), now - timedelta(days=2)),
        ('EMA Crossover', 'BTC/USDT', 62000, 0.02, 1240, 'closed', 45.00, now - timedelta(days=2), now - timedelta(days=1)),
    ]
    
    cursor.executemany('''
    INSERT INTO trades (strategy_name, symbol, entry_price, position_size, capital_used, status, pnl, entry_time, exit_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', closed_trades)

    # Simulacija: ODPRTI TREJDI (trenutno aktivni)
    open_trades = [
        ('MACD Trend', 'BTC/USDT', 64000, 0.1, 6400, 'open', 0, now - timedelta(hours=5), None),
        ('RSI Breakout', 'ETH/USDT', 3100, 0.5, 1550, 'open', 0, now - timedelta(hours=2), None)
    ]
    
    cursor.executemany('''
    INSERT INTO trades (strategy_name, symbol, entry_price, position_size, capital_used, status, pnl, entry_time, exit_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', open_trades)

    conn.commit()
    conn.close()
    print("Baza podatkov in testna zgodovina uspešno ustvarjeni!")

if __name__ == "__main__":
    create_database()