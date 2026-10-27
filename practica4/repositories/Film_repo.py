from bbdd import ConexionDB





class Film_repo:





    def __init__(self):
        pass

#1. Obtener el título de cada película y su categoría (relación entre film, film_category y category)
    def consultar_pelicula_titcat(self):
        consulta = (
            "SELECT f.title, c.name "
            "from film f "
            "inner join film_category fc "
            "on f.film_id = fc.film_id "
            "inner join category c "
            "on c.category_id = fc.category_id "
        )

        resultado = []
        with ConexionDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            for film in cursor:
                resultado.append(film)
            cursor.close()
        return resultado

#4. Mostrar el título de las películas junto con el idioma en que están disponibles (film + language)
    def mostrar_tit_idiom(self):
        consulta = (
            "select f.titile, l.name "
            "from film f "
            "inner join langauge l "
            "on f.language_id = l.language_id "
        )

        resultado = []
        with ConexionDB () as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            for film in consulta:
                resultado.append(film)
            cursor.close()
        return resultado


