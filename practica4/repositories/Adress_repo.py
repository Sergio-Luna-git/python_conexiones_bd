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


    def insercion(self):
        consulta = (
            "insert into country "
            " ( country ) "
            "values ('ValenciaLand') "
#Después podemos obtener su country_id. Creamos nueva ciudad asociada al país anterior “Ciudad del Abanico

        )

        consulta2 = (
            "insert into city "
            " ( city, country_id ) "
            "values ('Ciudad del Abanico',( select country_id from country where country = 'ValenciaLand')) "
        )

        consulta3 = (
            "SET @city_id = LAST_INSERT_ID() "
        )

#b. Nueva dirección asociada a la ciudad anterior usando el city_id: ('Calle de los Colibrís, 23', NULL, 'Centro', @city_id, '46000', '600123456')
        consulta4 = (
            "insert into address "
            "(address, address2, district, city_id, postal_code, phone, location) "
            "values ('Calle de los Colibrís, 23', NULL, 'Centro', @city_id, '46000', '600123456')"
        )

        with ConexionDB() as cnx:
            cursor =  cnx.cursor()
            cursor.execute(consulta)
            cursor.execute(consulta2)
            cursor.execute(consulta3)
            cursor.execute(consulta4)
            cnx.commit()
            cursor.close()

    def actualizar_ciuda(self):
        resultado = []
        ciudad_cambiar = input("Ingrese el nombre del ciudad a cambiar el nombre: ")
        nuevo_nombre = input("Introduce el nuevo nombre del ciudad: ")

        update = (
            "update city set "
            "city = %s "
            "where city = %s"
        )
        consulta = (
            "select city "
            "from city "
            "where city = %s"
        )

        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(update, (nuevo_nombre, ciudad_cambiar))
            cnx.commit()
            cursor.execute(consulta, (nuevo_nombre,))
            for row in cursor:
                resultado.append(row)
            cursor.close()
        return resultado

    def eliminar_cliente(self):
        cliente_eliminar = input("Ingrese el id del cliente a eliminar: ")
        delete3 = (
            "delete from customer "
            "where customer_id = %s"
        )
        delete2 = (
            "delete from rental "
            "where customer_id = %s"
        )
        delete1 = (
            "delete from payment "
            "where customer_id = %s"
        )

        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(delete1, (cliente_eliminar,))
            cursor.execute(delete2, (cliente_eliminar,))
            cursor.execute(delete3, (cliente_eliminar,))
            cnx.commit()
            cursor.close()

    def eliminar_categoria(self):
        consulta = (
            ""
        )
        delete1 = (
        "delete from film_category "
        "where category_id = (select category_id from category where name = 'Action') "
        )
        delete2 = (
            "delete from category "
            "where name = 'Action' "
        )

        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(delete1)
            cursor.execute(delete2)
            cursor.close()

