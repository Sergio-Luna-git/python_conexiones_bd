import os

from dotenv import load_dotenv


from bbdd import (
    ConexionBD,

)
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "33006")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "dbrootpass"),
    "database": os.getenv("DB_NAME", "sakila")
}

def paso(texto: str) -> None:
    print(f"\n=== {texto} ===")

def mian() -> None:
    paso("Intentar conexión con la Base de Datos")
    with ConexionBD(DB_CONFIG) as cnx:
        print(f"[] - Conexión establecida: {cnx.is_connected()} -> SERVIDO MySql: {cnx.get_server_info()}")


