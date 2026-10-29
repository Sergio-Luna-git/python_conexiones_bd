import os
from dotenv import load_dotenv
from bbdd import ConexionDB
from repositories.Adress_repo import AdressRepo
from repositories.Client_repo import Client_repo
from repositories.Film_repo import Film_repo
from repositories.Shop_repo import Shop_repo

load_dotenv()

def main():
    adress_repo = AdressRepo()
    client_repo = Client_repo()
    film_repo = Film_repo()
    shop_repo = Shop_repo()

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. AdressRepo - mostrar_direc_ciud")
        print("2. AdressRepo - insercion")
        print("3. AdressRepo - actualizar_ciuda")
        print("4. AdressRepo - eliminar_cliente")
        print("5. AdressRepo - eliminar_categoria")
        print("6. Client_repo - mostrar_client_direc")
        print("7. Client_repo - mostra_pago_cliente_rental")
        print("8. Film_repo - consultar_pelicula_titcat")
        print("9. Film_repo - mostrar_tit_idiom")
        print("10. Shop_repo - mostrar_stock_porpeli")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "0":
            print("Saliendo...")
            break
        elif opcion == "1":
            resultado = adress_repo.mostrar_direc_ciud()
            print("\nResultados:")
            for row in resultado:
                print(row)
        elif opcion == "2":
            adress_repo.insercion()
            print("\nInserción realizada.")
        elif opcion == "3":
            resultado = adress_repo.actualizar_ciuda()
            print("\nResultados:")
            for row in resultado:
                print(row)
        elif opcion == "4":
            adress_repo.eliminar_cliente()
            print("\nCliente eliminado.")
        elif opcion == "5":
            adress_repo.eliminar_categoria()
            print("\nCategoría eliminada.")
        elif opcion == "6":
            resultado = client_repo.mostrar_client_direc()
            print("\nResultados:")
            for row in resultado:
                print(row)
        elif opcion == "7":
            resultado = client_repo.mostra_pago_cliente_rental()
            print("\nResultados:")
            for row in resultado:
                print(row)
        elif opcion == "8":
            resultado = film_repo.consultar_pelicula_titcat()
            print("\nResultados:")
            for row in resultado:
                print(row)
        elif opcion == "9":
            resultado = film_repo.mostrar_tit_idiom()
            print("\nResultados:")
            for row in resultado:
                print(row)
        elif opcion == "10":
            resultado = shop_repo.mostrar_stock_porpeli()
            print("\nResultados:")
            for row in resultado:
                print(row)
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()