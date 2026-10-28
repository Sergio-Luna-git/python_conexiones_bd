from bbdd import ConexionDB

class Shop_repo:
    def __init__(self):
        pass

    def  mostrar_stock_porpeli(self):
        consulta = (
            "select f.title, (select group_concat( "
            "                 s.store_id, a.address ) "
            "                 from inventory i "
            "                 join store s "
            "                 on i.store_id = s.store_id "
            "                 join address a "
            "                 on s.address_id = a.address_id "
            "                 where i.film_id = f.film_id) as tiendas "
            "from film f "
        )

        resultado = []
        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            for row in cursor:
                resultado.append(row)
            cursor.close()
        return resultado