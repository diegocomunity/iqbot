import sqlite3
import pandas as pd
from models.trading_operation import TradingOperation
class TradingOperationRepository:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_operations (
                id INTEGER PRIMARY KEY,
                strategy_name TEXT NOT NULL,
                signal TEXT NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                result TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_all_operations(self):
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query('SELECT * FROM trading_operations', conn)
        conn.close()
        return df

    def save_operation(self, operation: TradingOperation):
        # Conectarse a la base de datos
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        # Insertar los datos de la operación en la tabla
        cursor.execute('''INSERT INTO trading_operations 
                          (strategy_name, action, price, timestamp, result) 
                          VALUES (?, ?, ?, ?, ?)''', 
                       (operation.strategy_name, operation.action, operation.price, operation.timestamp, operation.result))

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        print("Operación guardada en la base de datos.")

