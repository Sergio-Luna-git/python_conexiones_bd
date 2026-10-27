from bbdd import ConexionDB

class AdressRepo:
    def __init__(self):
        pass

    #. Ver las direcciones junto con el nombre de la ciudad (address + city).
    def mostrar_direc_ciud(self):
        consulta = (
            "select a.address, a.address2, c.city"
            "from adress a"
            "join city c"
            "on a.city_id = c.city_id"
        )

        resultado = []
        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            for row in cursor:
                resultado.append(row)
            cursor.close()
        return resultado
