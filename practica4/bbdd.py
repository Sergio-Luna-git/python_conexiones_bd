"""bbdd.py — Clase de conexión a la base de datos."""

import os
import mysql.connector
from mysql.connector import errorcode


class ConexionDB:
    """Gestor de contexto para una conexión MySQL.

    Uso:
        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            ...
    """
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "33006")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "dbrootpass"),
        "database": os.getenv("DB_NAME", "sakila")
    }

    def __init__(self, config: dict = None):
        self.config = config if config is not None else self.DB_CONFIG
        self.cnx = None

    def __enter__(self) -> mysql.connector.MySQLConnection:
        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError("Usuario o contraseña incorrectos") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError(
                    f"La base de datos '{self.config.get('database')}' no existe."
                ) from err
            raise
        return self.cnx

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.cnx is not None and self.cnx.is_connected():
            self.cnx.close()
