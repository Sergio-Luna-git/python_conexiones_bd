import os

from dotenv import load_dotenv


from bbdd import (
    ConexionBD,

)
load_dotenv()

def paso(texto: str) -> None:
    print(f"\n=== {texto} ===")

def main() -> None:
    paso("Intentar conexión con la Base de Datos")
    with ConexionBD(DB_CONFIG) as cnx:
        print(f"[] - Conexión establecida: {cnx.is_connected()}")


#if __name__ == "__main__":
 #   main()