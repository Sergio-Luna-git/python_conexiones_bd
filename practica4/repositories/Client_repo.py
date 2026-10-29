from bbdd import ConexionDB

class Client_repo:
    def __init__(self):
        pass

#2. Mostrar el nombre completo del cliente y la dirección asociada (customer + address)
    def mostrar_client_direc(self):

        consulta = (
            "select c.first_name, c.last_name, a.address, a.address2 "
            "from customer c"
            "join address a"
            "on c.address_id = a.address_id"
        )

        resultado = []
        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            for row in cursor:
                resultado.append(row)
            cursor.close()
        return resultado

    #6. Obtener los pagos realizados por cada cliente en sus alquileres (payment, rental, customer).
    def mostra_pago_cliente_rental(self):
        consulta = (
            "select p.payment_id, p.amount as 'Total:', r.rental_id"
            "from payment p"
            "join customer c"
            "on p.customer_id = c.customer_id"
            "join rental r"
            "on c.customer_id = r.customer_id"
        )

        resultado = []

        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            for row in cursor:
                resultado.append(row)
            cursor.close()
        return resultado

