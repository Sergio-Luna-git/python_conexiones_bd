"""demo_tema2.py — Recorre, paso a paso, todo lo visto en el Tema 2
(Acceso a Bases de Datos Relacionales) contra la base de datos
'employees' creada por schema_employees.sql.

Antes de ejecutar:
    1. mysql -u root -p < schema_employees.sql
    2. cp .env.example .env   y rellena tus credenciales
    3. pip install -r requirements.txt
    4. python demo_tema2.py
"""

import os
from datetime import date

from dotenv import load_dotenv

from bbdd import (
    ConexionBD,
    Empleado,
    RepositorioEmpleados,
    RepositorioFunciones,
    RepositorioProcedimientos,
    Transaccion,
)

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "33006")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "employees"),
}


def paso(titulo: str) -> None:
    print(f"\n=== {titulo} ===")


def main() -> None:
    repo = RepositorioEmpleados(DB_CONFIG)

    # ---------- 1. Conexión ----------
    paso("1. Probando la conexión")
    with ConexionBD(DB_CONFIG) as cnx:
        print(f"Conectado: {cnx.is_connected()} (servidor MySQL {cnx.get_server_info()})")

    # ---------- 2. Insertar un nuevo empleado ----------
    paso("2. Insertando un nuevo empleado")
    nuevo = Empleado(
        nombre="Elena",
        apellido="Roig",
        fecha_nacimiento=date(1994, 4, 18),
        genero="F",
        fecha_contratacion=date.today(),
    )
    nuevo = repo.insertar(nuevo)
    repo.asignar_departamento(nuevo.emp_no, "d003", date.today())
    repo.insertar_salario(nuevo.emp_no, 27000, date.today())
    print(f"Empleado insertado con emp_no={nuevo.emp_no}, departamento={repo.departamento_actual(nuevo.emp_no)}")

    # ---------- 3. Consultar ----------
    paso("3. Empleados contratados en 2019")
    for emp in repo.buscar_contratados_entre(date(2019, 1, 1), date(2019, 12, 31)):
        print(f"  {emp.emp_no}: {emp.apellido}, {emp.nombre} — {emp.fecha_contratacion}")

    # ---------- 4. Actualizar ----------
    paso("4. Actualizando el apellido del empleado insertado")
    repo.actualizar_apellido(nuevo.emp_no, "Roig Martí")
    actualizado = repo.buscar_contratados_entre(date.today(), date.today())
    print(f"  Apellido actual: {actualizado[0].apellido if actualizado else '(no encontrado)'}")

    # ---------- 5. Transacción con éxito ----------
    paso("5. Transacción: mover al empleado de d003 a d001")
    with ConexionBD(DB_CONFIG) as cnx:
        with Transaccion(cnx) as cursor:
            repo.mover_de_departamento(cursor, nuevo.emp_no, "d003", "d001", date.today())
    print(f"  Departamento tras la transacción: {repo.departamento_actual(nuevo.emp_no)}")

    # ---------- 6. Transacción con error (demuestra el rollback) ----------
    paso("6. Transacción que falla a propósito (debe deshacerse por completo)")
    dept_antes = repo.departamento_actual(nuevo.emp_no)
    try:
        with ConexionBD(DB_CONFIG) as cnx:
            with Transaccion(cnx) as cursor:
                cursor.execute(
                    "UPDATE dept_emp SET to_date = %s WHERE emp_no = %s AND dept_no = %s AND to_date = %s",
                    (date.today(), nuevo.emp_no, "d001", date(9999, 1, 1)),
                )
                # dept_no inventado: la FK de dept_emp lo rechaza y debe
                # deshacer también el UPDATE anterior
                cursor.execute(
                    "INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
                    (nuevo.emp_no, "zzzz", date.today(), date(9999, 1, 1)),
                )
    except Exception as err:
        print(f"  Error esperado capturado: {err}")
    dept_despues = repo.departamento_actual(nuevo.emp_no)
    print(f"  Departamento antes: {dept_antes} | después del rollback: {dept_despues} (deben coincidir)")

    # ---------- 7. Procedimiento almacenado ----------
    paso("7. Procedimiento almacenado 'multiply'")
    procs = RepositorioProcedimientos(DB_CONFIG)
    print(f"  multiply(6, 7) = {procs.multiplicar(6, 7)}")

    # ---------- 8. Función almacenada ----------
    paso("8. Función almacenada 'antiguedad_anios'")
    funcs = RepositorioFunciones(DB_CONFIG)
    print(f"  Antigüedad del empleado 10001: {funcs.antiguedad_anios(10001)} años")

    # ---------- 9. Limpieza ----------
    paso("9. Eliminando el empleado de prueba (dept_emp y salaries caen en cascada)")
    repo.eliminar(nuevo.emp_no)
    print(f"  Empleado {nuevo.emp_no} eliminado.")

    print("\nDemo completada sin errores inesperados.")


if __name__ == "__main__":
    main()
